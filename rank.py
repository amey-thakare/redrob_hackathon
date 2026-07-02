import pandas as pd
import csv
import argparse
from src.semantic_matcher import compute_semantic_scores
from src.loader import load_candidates
from src.scorer import compute_score
from src.reasoning import generate_reasoning
from src.semantic_reranker import rerank as semantic_rerank
import time
def normalize(values):

    mn = min(values)
    mx = max(values)

    if mx == mn:
        return [1.0] * len(values)

    return [
        (v - mn) / (mx - mn)
        for v in values
    ]
parser = argparse.ArgumentParser()

parser.add_argument(
    "--candidates",
    default="data/candidates.jsonl"
)

parser.add_argument(
    "--out",
    default="outputs/submission.csv"
)

args = parser.parse_args()

candidates = load_candidates(args.candidates)

results = []

stage1_start = time.perf_counter()

for i, c in enumerate(candidates):

    if i % 1000 == 0:

        elapsed = time.perf_counter() - stage1_start

        print(
            f"{i}/{len(candidates)} | "
            f"{elapsed:.2f}s"
        )

    score = compute_score(c)

    results.append({
        "candidate": c,
        "candidate_id": c["candidate_id"],
        "score": score,
        "reasoning": generate_reasoning(c)
    })

print(
    f"\nStage 1 completed in "
    f"{time.perf_counter()-stage1_start:.2f}s\n"
)


print(len(results))

# Sort by score
results = sorted(
    results,
    key=lambda x: (-x["score"], x["candidate_id"])
)
# -----------------------------
# Stage 1: Rule-based ranking
# -----------------------------

top500 = results[:500]

# -----------------------------
# Stage 2: Semantic ranking
# -----------------------------

print("Computing semantic scores...")

semantic_scores = compute_semantic_scores(
    [row["candidate"] for row in top500]
)

for row, score in zip(top500, semantic_scores):

    row["semantic_score"] = score

top500 = sorted(
    top500,
    key=lambda x: (
        x["score"] + 0.15 * x["semantic_score"]
    ),
    reverse=True
)

# Keep best 200
top120 = top500[:120]

# -----------------------------
# Stage 3: CrossEncoder reranking
# -----------------------------
print("Starting reranking...")

top120 = semantic_rerank(top120)

print("Reranking completed")

# Combine all three stages
rule_scores = [r["score"] for r in top120]
semantic_scores = [r["semantic_score"] for r in top120]
reranker_scores = [r["reranker_score"] for r in top120]

rule_scores = normalize(rule_scores)
semantic_scores = normalize(semantic_scores)
reranker_scores = normalize(reranker_scores)

for i, row in enumerate(top120):

    row["final_score"] = (
        0.25 * rule_scores[i] +
        0.20 * semantic_scores[i] +
        0.55 * reranker_scores[i]
    )

top120 = sorted(
    top120,
    key=lambda x: x["final_score"],
    reverse=True
)

top100 = top120[:100]

# Assign rank
for i, row in enumerate(top100):
    row["rank"] = i + 1

# Normalize scores
max_score = top100[0]["final_score"]
min_score = top100[-1]["final_score"]

print("Max final score:", max_score)
print("Min final score:", min_score)

if max_score != min_score:
    for row in top100:
        row["score"] = round(
            (row["final_score"] - min_score)
            /
            (max_score - min_score),
            4
        )
else:
    for row in top100:
        row["score"] = 1.0

# Create dataframe
submission = pd.DataFrame(top100)

# Arrange columns
submission = submission[
    ["candidate_id", "rank", "score", "reasoning"]
]

# Save csv
submission.to_csv(
    args.out,
    index=False,
    quoting=csv.QUOTE_ALL
)

print(submission.head(10))

print("\nTop 20 Candidates\n")

for row in top100[:20]:

    c = row["candidate"]
    profile = c["profile"]

    print("=" * 80)

    print("Candidate ID :", row["candidate_id"])
    print("Rank         :", row["rank"])
    print("Score        :", row["score"])

    print()

    print("Title        :", profile["current_title"])
    print("Experience   :", profile["years_of_experience"])
    print("Industry     :", profile["current_industry"])

    print()

    print("Skills")

    for skill in c["skills"]:

        print(
            "-",
            skill["name"]
        )

    print()

    print("Reasoning")

    print(row["reasoning"])

    print()