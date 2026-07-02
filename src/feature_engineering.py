"""Job matching scoring module for candidate evaluation."""

from src.honeypot_detector import honeypot_penalty
from src.job_matcher import compute_job_match

from src.product_company_detector import (
    get_product_background_score,
    ranking_system_score,
    product_mindset_score,
    evaluation_framework_score,
    production_system_score
)

from src.job_loader import load_job_profile

JOB = load_job_profile()

required_skills = {
    skill.lower()
    for skill in JOB["required_skills"]
}

preferred_skills = {
    skill.lower()
    for skill in JOB["preferred_skills"]
}

skill_weights = {
    k.lower(): v
    for k, v in JOB["skill_weights"].items()
}

required_experience = int(JOB["experience"])

required_seniority = JOB["seniority"].lower()

role = JOB["role"]
required_seniority = JOB["seniority"].lower()

def get_title_score(title):

    title = title.lower()

    target = role.lower()

    if target in title:
        return 1.0

    if any(word in title for word in target.split()):
        return 0.8

    ai_titles = [
        "ai engineer",
        "machine learning engineer",
        "ml engineer",
        "llm engineer",
        "applied scientist",
        "nlp engineer",
        "search engineer",
        "retrieval engineer",
    ]

    if any(t in title for t in ai_titles):
        return 0.7

    return 0.3

# Title scoring



def get_seniority_score(title):

    title = title.lower()

    if required_seniority in title:
        return 1.0

    seniority_order = {
        "intern": 0,
        "junior": 1,
        "associate": 2,
        "mid": 3,
        "senior": 4,
        "lead": 5,
        "staff": 6,
        "principal": 7
    }

    candidate_level = 0

    for level in seniority_order:
        if level in title:
            candidate_level = seniority_order[level]
            break

    required_level = seniority_order.get(required_seniority, 0)

    diff = candidate_level - required_level

    if diff >= 0:
        return 1.0
    elif diff == -1:
        return 0.8
    else:
        return 0.5


# Experience scoring
def get_experience_score(years_of_experience):

    diff = years_of_experience - required_experience

    if diff >= 2:
        return 1.0

    elif diff >= 0:
        return 0.9

    elif diff == -1:
        return 0.8

    elif diff == -2:
        return 0.6

    return 0.3


SKILL_ALIASES = {

    # LLM
    "llms": "llm",
    "fine-tuning llms": "llm",
    "hugging face transformers": "llm",
    "transformers": "llm",

    # Embeddings
    "sentence transformers": "embeddings",
    "semantic search": "embeddings",
    "vector search": "embeddings",
    "pgvector": "embeddings",
    "faiss": "embeddings",
    "milvus": "embeddings",
    "weaviate": "embeddings",

    # RAG
    "information retrieval": "rag",
    "retrieval": "rag",
    "retrieval systems": "rag",

    # FastAPI
    "rest apis": "fastapi",

    # PyTorch
    "torch": "pytorch",
}

# Skill scoring
def get_skill_score(skills):
    """Score based on required job skills."""

    matched = 0

    for skill in skills:

        name = skill["name"].lower()

        name = SKILL_ALIASES.get(
        name,
        name
    )

        if name in required_skills:
            matched += 1

    if len(required_skills) == 0:
        return 0

    return matched / len(required_skills)


def get_bonus_score(skills):

    total = sum(skill_weights.values())

    score = 0

    seen = set()

    for skill in skills:

        name = skill["name"].lower()

        name = SKILL_ALIASES.get(
            name,
            name
        )

        if name in seen:
            continue

        score += skill_weights.get(name, 0)

        seen.add(name)

    return score / max(total, 1)


def get_rare_skill_score(skills):

    top = sorted(
        skill_weights,
        key=skill_weights.get,
        reverse=True
    )[:5]

    found = set()

    for skill in skills:

        name = skill["name"].lower()

        name = SKILL_ALIASES.get(
            name,
            name
        )

        if name in top:
            found.add(name)

    return len(found) / max(
        len(top),
        1
    )


# Signal scoring
def get_industry_score(industry):

    industry = industry.lower()

    if "ai/ml" in industry:
        return 1.0

    elif "conversational ai" in industry:
        return 0.95

    elif "voice ai" in industry:
        return 0.95

    elif "healthtech ai" in industry:
        return 0.90

    elif "ai services" in industry:
        return 0.90

    elif "software" in industry:
        return 0.85

    elif "e-commerce" in industry:
        return 0.75

    elif "media" in industry:
        return 0.70

    elif "gaming" in industry:
        return 0.65

    elif "fintech" in industry:
        return 0.65

    elif "it services" in industry:
        return 0.60

    return 0.50

def get_open_to_work_score(flag):
    """Score based on open to work flag."""
    return 1.0 if flag else 0.0


def get_notice_score(days):
    """Score based on notice period."""
    if days <= 15:
        return 1.0
    elif days <= 30:
        return 1.0
    elif days <= 60:
        return 0.7
    elif days <= 90:
        return 0.4

    return 0.0


def get_response_score(rate):
    """Score based on recruiter response rate."""
    return rate


def get_github_score(score):
    """Score based on GitHub activity score."""
    if score == -1:
        return 0.0

    return score / 100


def get_saved_score(saved):
    """Score based on times saved by recruiters."""
    return min(saved / 80, 1.0)


def get_search_score(searches):
    """Score based on search appearance count."""
    return min(searches / 1490, 1.0)


def get_company_size_score(size):

    size = size.lower()

    if "enterprise" in size:
        return 1.0

    if "1000+" in size:
        return 0.9

    if "500-1000" in size:
        return 0.8

    if "100-500" in size:
        return 0.7

    if "10-100" in size:
        return 0.6

    return 0.5

def get_skill_quality_score(skills):

    PROFICIENCY = {
        "beginner": 0.25,
        "intermediate": 0.50,
        "advanced": 0.80,
        "expert": 1.00,
    }

    if not skills:
        return 0

    total = 0

    for skill in skills:

        proficiency = PROFICIENCY.get(
            skill.get(
                "proficiency",
                ""
            ).lower(),
            0.5
        )

        duration = min(
            skill.get(
                "duration_months",
                12
            ) / 48,
            1.0
        )

        total += proficiency * duration

    return min(
        total / len(skills),
        1.0
    )
# Feature extraction
def extract_features(candidate):
    
    """Extract all features for a candidate."""
    profile = candidate["profile"]
    signals = candidate["redrob_signals"]
    skills = candidate["skills"]

    features = {
    "product_background_score": get_product_background_score(candidate),
    "ranking_system_score": ranking_system_score(candidate),
    "product_mindset_score": product_mindset_score(candidate),
    "evaluation_framework_score": evaluation_framework_score(candidate),
    "production_system_score": production_system_score(candidate),
    "honeypot_penalty": honeypot_penalty(candidate),
    "job_match_score": compute_job_match(candidate),
    "title_score": get_title_score(profile["current_title"]),
    "seniority_score": get_seniority_score(profile["current_title"]),
    "experience_score": get_experience_score(profile["years_of_experience"]),

    "ai_skill_score": get_skill_score(
    skills
),
    "skill_quality_score": get_skill_quality_score(skills),
    "bonus_score": get_bonus_score(skills),
    "rare_skill_score": get_rare_skill_score(skills),

    "industry_score": get_industry_score(profile["current_industry"]),
    "open_to_work": get_open_to_work_score(signals["open_to_work_flag"]),
    "notice_score": get_notice_score(signals["notice_period_days"]),
    "response_score": get_response_score(signals["recruiter_response_rate"]),
    "github_score": get_github_score(signals["github_activity_score"]),
    "saved_score": get_saved_score(signals["saved_by_recruiters_30d"]),
    "search_score": get_search_score(signals["search_appearance_30d"]),
    "company_size_score": get_company_size_score(profile["current_company_size"]),


}
    return features
