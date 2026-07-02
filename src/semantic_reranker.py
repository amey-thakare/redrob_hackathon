from sentence_transformers import CrossEncoder

from src.semantic_matcher import (
    build_job_text,
    build_candidate_text,
)

MODEL = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    max_length=512,
)

JOB_TEXT = build_job_text()


def rerank(candidates):
    """
    CrossEncoder reranking for Top-K candidates.
    """

    pairs = [
        (
            JOB_TEXT,
            build_candidate_text(row["candidate"])
        )
        for row in candidates
    ]

    scores = MODEL.predict(
        pairs,
        batch_size=32,
        show_progress_bar=False,
    )

    scores = scores.tolist()

    mn = min(scores)
    mx = max(scores)

    if mx > mn:
        scores = [
            (s - mn) / (mx - mn)
            for s in scores
        ]
    else:
        scores = [1.0] * len(scores)

    for row, score in zip(candidates, scores):
        row["reranker_score"] = float(score)

    return candidates