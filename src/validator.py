AI_SKILLS = {
    "Python",
    "PyTorch",
    "TensorFlow",
    "Transformers",
    "LLM",
    "RAG",
    "LangChain",
    "Pinecone",
    "Qdrant",
    "FAISS",
    "Embeddings"
}
SERVICE_COMPANIES = {
    "TCS",
    "Infosys",
    "Wipro",
    "Cognizant",
    "Capgemini",
    "Accenture",
}

NON_AI_TITLES = {
    "Marketing Manager",
    "HR Manager",
    "Content Writer",
    "Graphic Designer",
    "Accountant",
    "Sales Executive",
    "Customer Support"
}


def impossible_profile(candidate):

    profile = candidate["profile"]
    title = profile["current_title"]

    # Senior title with very low experience
    if (
        "Senior" in title
        and profile["years_of_experience"] < 2
    ):
        return True

    # Career history cannot exceed reported experience
    total_months = sum(
        job["duration_months"]
        for job in candidate["career_history"]
    )

    if total_months / 12 > profile["years_of_experience"] + 2:
        return True

    # Too many expert skills
    expert_count = sum(
        1
        for skill in candidate["skills"]
        if skill["proficiency"] == "expert"
    )

    if expert_count > 8:
        return True

    # Expert skills with zero duration
    suspicious = sum(
        1
        for skill in candidate["skills"]
        if (
            skill["proficiency"] == "expert"
            and skill.get("duration_months", 12) == 0
        )
    )

    if suspicious >= 3:
        return True

    # Non-AI title with many AI skills
    ai_count = sum(
        1
        for skill in candidate["skills"]
        if skill["name"] in AI_SKILLS
    )

    if (
        title in NON_AI_TITLES
        and ai_count >= 8
    ):
        return True

    return False

def pure_service_background(candidate):

    history = candidate["career_history"]

    return (
        len(history) > 0
        and all(
            job["company"] in SERVICE_COMPANIES
            for job in history
        )
    )




def job_hopper(candidate):

    history = candidate["career_history"]

    if len(history) < 3:
        return False

    return sum(
        job["duration_months"] < 18
        for job in history
    ) >= 3

from datetime import datetime

def inactive_candidate(candidate):

    signals = candidate["redrob_signals"]

    last_active = datetime.strptime(
        signals["last_active_date"],
        "%Y-%m-%d"
    )

    today = datetime(2025, 12, 31)

    days_inactive = (today - last_active).days

    return days_inactive > 180



 

def suspicious_career_history(candidate):

    profile = candidate["profile"]

    total_months = sum(
    job["duration_months"]
    for job in candidate["career_history"]
)

    years_from_jobs = total_months / 12

    reported_years = profile["years_of_experience"]

    difference = abs(years_from_jobs - reported_years)

    return difference > 3

BAD_TITLE_KEYWORDS = {
    "support",
    "sales",
    "marketing",
    "finance",
    "accountant",
    "customer",
    "content",
    "mechanical",
    "civil",
    "electrical",
    "business analyst",
    "hr",
    "recruiter",
    "operations",
    "qa tester",
    "manual tester",
    "customer success",
}


def bad_title(candidate):

    title = candidate["profile"]["current_title"].lower()

    return any(word in title for word in BAD_TITLE_KEYWORDS)

def title_skill_mismatch(candidate):

    title = candidate["profile"]["current_title"].lower()

    ai_titles = [
        "ai",
        "ml",
        "machine learning",
        "nlp",
        "data scientist",
        "applied scientist",
        "research engineer"
    ]

    has_ai_title = any(x in title for x in ai_titles)

    ai_skills = {
        "Python",
        "LLM",
        "LangChain",
        "PyTorch",
        "RAG",
        "Embeddings",
        "FAISS",
        "Pinecone",
        "Qdrant"
    }

    matched = sum(
        1
        for skill in candidate["skills"]
        if skill["name"] in ai_skills
    )

    if has_ai_title and matched < 2:
        return True

    return False