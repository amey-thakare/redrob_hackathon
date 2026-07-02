"""
Semantic Skill Matcher

This module performs hybrid skill matching using:
1. Exact Match
2. Skill Normalization
3. Related Technology Matching
4. Embedding Similarity (BGE)
"""
from src.cache import cached_encode

from src.cache import cached_encode
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.ontology import NORMALIZATION, RELATED_SKILLS

# Load model only once
MODEL = SentenceTransformer("BAAI/bge-small-en-v1.5")


def normalize(skill: str) -> str:
    """
    Normalize a skill name.

    Example:
    Retrieval Augmented Generation -> rag
    Amazon Web Services -> aws
    """

    skill = skill.lower().strip()

    return NORMALIZATION.get(skill, skill)


def semantic_skill_score(candidate_skills, required_skills):
    """
    Computes semantic similarity score between candidate skills
    and required job skills.

    Returns:
        float between 0 and 1
    """

    # Candidate skill names
    candidate = [
        normalize(skill["name"])
        for skill in candidate_skills
    ]

    # Required skill names
    required = [
        normalize(skill)
        for skill in required_skills
    ]

    if not candidate or not required:
        return 0.0

    final_scores = []
    remaining_required = []

    ########################################################
    # Step 1 : Exact + Related Technology Matching
    ########################################################

    for req in required:

        # Exact Match
        if req in candidate:
            final_scores.append(1.0)
            continue

        # Related Technologies
        related = RELATED_SKILLS.get(req, set())

        if any(skill in related for skill in candidate):
            final_scores.append(0.85)
            continue

        # Needs semantic matching
        final_scores.append(None)
        remaining_required.append(req)

    ########################################################
    # Step 2 : Everything matched already
    ########################################################

    if not remaining_required:
        return float(np.mean(final_scores))

    ########################################################
    # Step 3 : Embedding Matching
    ########################################################

    candidate_embeddings = [
    cached_encode(MODEL, skill)
    for skill in candidate
]

    required_embeddings = [
    cached_encode(MODEL, skill)
    for skill in remaining_required
]

    similarity_matrix = cosine_similarity(
        required_embeddings,
        candidate_embeddings
    )

    embedding_scores = similarity_matrix.max(axis=1)

    ########################################################
    # Step 4 : Merge Scores
    ########################################################

    idx = 0

    for i in range(len(final_scores)):

        if final_scores[i] is None:

            similarity = float(embedding_scores[idx])

            # Ignore weak semantic matches
            if similarity < 0.60:
                similarity = 0.0

            final_scores[i] = similarity

            idx += 1

    ########################################################
    # Step 5 : Final Score
    ########################################################

    return round(float(np.mean(final_scores)), 4)


############################################################
# Test
############################################################

if __name__ == "__main__":

    candidate_skills = [
        {"name": "Python"},
        {"name": "Milvus"},
        {"name": "Retrieval Augmented Generation"},
        {"name": "FastAPI"},
        {"name": "Docker"},
        {"name": "LlamaIndex"},
    ]

    required_skills = {
        "Python",
        "RAG",
        "FAISS",
        "FastAPI",
        "LangChain",
    }

    score = semantic_skill_score(
        candidate_skills,
        required_skills
    )

    print(f"\nSemantic Skill Score: {score}")