"""
Semantic Job Matcher

Computes semantic similarity between a candidate profile
and the job description using BGE embeddings.
"""
from src.cache import cached_encode
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.job_loader import load_job_profile

# ---------------------------------------------------
# Load embedding model only once
# ---------------------------------------------------

MODEL = SentenceTransformer("BAAI/bge-small-en-v1.5")

# ---------------------------------------------------
# Load Job
# ---------------------------------------------------

JOB = load_job_profile()


def build_job_document():
    """
    Convert job profile into a single text document.
    """

    parts = []

    parts.append(JOB.get("role", ""))

    parts.append(JOB.get("seniority", ""))

    parts.append(
        f"Experience {JOB.get('experience','')} years"
    )

    parts.extend(
        JOB.get("required_skills", [])
    )

    parts.extend(
        JOB.get("preferred_skills", [])
    )

    return "\n".join(parts)


JOB_DOCUMENT = build_job_document()

JOB_EMBEDDING = MODEL.encode(
    JOB_DOCUMENT,
    normalize_embeddings=True
)


# ---------------------------------------------------
# Candidate Document
# ---------------------------------------------------

def candidate_to_document(candidate):
    """
    Convert an entire candidate profile into text.
    """

    profile = candidate["profile"]

    parts = []

    # Title
    parts.append(
        profile.get("current_title", "")
    )

    # Industry
    parts.append(
        profile.get("current_industry", "")
    )

    # Experience
    parts.append(
        f"{profile.get('years_of_experience',0)} years experience"
    )

    # Skills
    for skill in candidate.get("skills", []):

        parts.append(
            skill.get("name", "")
        )

    # Career History
    for job in candidate.get("career_history", []):

        parts.append(
            job.get("title", "")
        )

        parts.append(
            job.get("description", "")
        )

    return "\n".join(parts)


# ---------------------------------------------------
# Semantic Matching
# ---------------------------------------------------

def compute_semantic_job_match(candidate):
    """
    Returns semantic similarity between
    candidate and job.

    Output:
        float (0-1)
    """

    candidate_document = candidate_to_document(
        candidate
    )

    candidate_embedding = cached_encode(
    MODEL,
    candidate_document
)

    similarity = cosine_similarity(
        [JOB_EMBEDDING],
        [candidate_embedding]
    )[0][0]

    # Clamp
    similarity = max(0.0, similarity)

    similarity = min(1.0, similarity)

    return round(float(similarity), 4)


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    dummy_candidate = {

        "profile": {

            "current_title": "Senior AI Engineer",

            "current_industry": "AI/ML",

            "years_of_experience": 6
        },

        "skills": [

            {"name": "Python"},
            {"name": "LangChain"},
            {"name": "FAISS"},
            {"name": "RAG"},
            {"name": "FastAPI"},
            {"name": "Embeddings"},
        ],

        "career_history": [

            {

                "title": "ML Engineer",

                "description":
                "Built production RAG pipelines using LangChain and FAISS."

            }

        ]

    }

    score = compute_semantic_job_match(
        dummy_candidate
    )

    print("Semantic Job Match:", score)

def get_job_document():
    return JOB_DOCUMENT