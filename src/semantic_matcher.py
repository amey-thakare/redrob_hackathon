from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from src.job_loader import load_job_profile

# Load embedding model once
model = SentenceTransformer("BAAI/bge-large-en-v1.5")
model.eval()

# Load job profile once
JOB = load_job_profile()


def build_job_text():
    """Convert structured job profile into text."""

    text = ""

    text += f"Role: {JOB.get('role', '')}\n"
    text += f"Seniority: {JOB.get('seniority', '')}\n"
    text += f"Experience: {JOB.get('experience', '')} years\n"

    text += "\nRequired Skills\n"

    for skill in JOB.get("required_skills", []):
        text += f"{skill}\n"

    text += "\nPreferred Skills\n"

    for skill in JOB.get("preferred_skills", []):
        text += f"{skill}\n"

    return text


def build_candidate_text(candidate):
    """Convert candidate into a semantic document."""

    profile = candidate.get("profile", {})

    text = ""

    # Basic profile
    text += f"Headline: {profile.get('headline', '')}\n"
    text += f"Summary: {profile.get('summary', '')}\n"
    text += f"Current Title: {profile.get('current_title', '')}\n"
    text += f"Industry: {profile.get('current_industry', '')}\n"
    text += f"Experience: {profile.get('years_of_experience', '')} years\n"
    text += f"Company: {profile.get('current_company_name', '')}\n"

    # Career History
    text += "\nCareer History\n"

    for job in candidate.get("career_history", []):

        text += f"Title: {job.get('title', '')}\n"
        text += f"Company: {job.get('company_name', '')}\n"
        text += f"Description: {job.get('description', '')}\n"

    # Skills
    text += "\nSkills\n"

    for skill in candidate.get("skills", []):

        text += f"{skill.get('name', '')}\n"

    # Education (if available)
    education = candidate.get("education", [])

    if education:

        text += "\nEducation\n"

        for edu in education:

            text += f"{edu.get('degree', '')}\n"
            text += f"{edu.get('institution', '')}\n"

    # Certifications (if available)
    certifications = candidate.get("certifications", [])

    if certifications:

        text += "\nCertifications\n"

        for cert in certifications:

            text += f"{cert.get('name', '')}\n"

    # Projects (if available)
    projects = candidate.get("projects", [])

    if projects:

        text += "\nProjects\n"

        for project in projects:

            text += f"{project.get('title', '')}\n"
            text += f"{project.get('description', '')}\n"

    return text


# Compute job embedding only once
JOB_EMBEDDING = model.encode(
    build_job_text(),
    normalize_embeddings=True
)

def compute_semantic_scores(candidates):
    """
    Compute semantic scores for multiple candidates in one batch.
    """

    texts = []

    for candidate in candidates:
        texts.append(
            build_candidate_text(candidate)
        )

    embeddings = model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    similarities = cos_sim(
        JOB_EMBEDDING,
        embeddings
    )[0]

    scores = []

    for similarity in similarities:

        score = (similarity.item() + 1) / 2

        score = max(
            0.0,
            min(1.0, score)
        )

        scores.append(score)

    return scores
