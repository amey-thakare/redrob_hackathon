from src.job_loader import load_job_profile
from src.embedding_matcher import semantic_skill_score

def generate_reasoning(candidate):

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]
    skills = candidate["skills"]

    strengths = []
    concerns = []

    # --------------------------------------------------
    # Intro
    # --------------------------------------------------

    reasoning = (
        f"{profile['current_title']} with "
        f"{profile['years_of_experience']:.1f} years of experience."
    )

    # --------------------------------------------------
    # Semantic Skill Matching
    # --------------------------------------------------

    from src.job_loader import load_job_profile

    JOB = load_job_profile()

    required = (
    set(JOB["required_skills"])
    | set(JOB["preferred_skills"])
)

    required_lower = {
    s.lower()
    for s in required
}

    aliases = {
    "llms": "llm",
    "fine-tuning llms": "llm",
    "hugging face transformers": "transformers",
    "information retrieval": "rag",
    "retrieval": "rag",
    "semantic search": "embeddings",
    "vector search": "embeddings",
    "sentence transformers": "embeddings",
    "pgvector": "embeddings",
}

    matched = []

    for skill in skills:

        name = skill["name"].lower()

        name = aliases.get(
        name,
        name
    )

    # Exact match
        if name in required_lower:

            matched.append(
            skill["name"]
        )

            continue

    # Semantic match
        score = semantic_skill_score(
        [skill],
        required,
    )

        if score >= 0.80:

            matched.append(
            skill["name"]
        )

    matched = list(dict.fromkeys(matched))

    if matched:

        strengths.append(
        "Core AI skills: " +
        ", ".join(matched[:6])
    )

    # --------------------------------------------------
    # Retrieval Stack
    # --------------------------------------------------

    retrieval = {
        "FAISS",
        "Pinecone",
        "Qdrant",
        "Embeddings",
        "Elasticsearch",
        "Haystack",
        "LlamaIndex",
        "Vector Search",
        "Semantic Search",
        "Sentence Transformers",
        "pgvector",
        "Milvus",
        "Weaviate",
        "OpenSearch"
    }

    retrieval_found = []

    for skill in skills:

        if skill["name"] in retrieval:
            retrieval_found.append(skill["name"])

    if retrieval_found:

        strengths.append(
    "Retrieval stack: " +
    ", ".join(retrieval_found[:6])
)

    # --------------------------------------------------
    # Production Systems
    # --------------------------------------------------

    keywords = {
        "production",
        "pipeline",
        "deployment",
        "distributed",
        "latency",
        "serving",
        "microservice",
        "scale",
        "real-time"
    }

    production = False

    for job in candidate.get("career_history", []):

        text = (
            job.get("title", "") +
            " " +
            job.get("description", "")
        ).lower()

        if any(keyword in text for keyword in keywords):

            production = True
            break

    if production:

        strengths.append(
            "Production ML deployment experience"
        )

    # --------------------------------------------------
    # Recruiter Signals
    # --------------------------------------------------

    if signals["open_to_work_flag"]:
        strengths.append("Open to work")

    if signals["notice_period_days"] <= 30:
        strengths.append("Short notice period")

    if signals["saved_by_recruiters_30d"] >= 10:
        strengths.append("Frequently saved by recruiters")

    if signals["recruiter_response_rate"] >= 0.80:
        strengths.append("High recruiter response rate")

    # --------------------------------------------------
    # Concerns
    # --------------------------------------------------

    if signals["notice_period_days"] > 90:
        concerns.append("Long notice period")

    if signals["github_activity_score"] <= 0:
        concerns.append("Limited GitHub activity")

    if len(matched) <= 2:
        concerns.append("Limited overlap with required AI stack")

    elif len(matched) >= 6:
        strengths.append("Strong alignment with required AI stack")
    # --------------------------------------------------
    # Final Reasoning
    # --------------------------------------------------

    if strengths:

        reasoning += (
            " Strengths: " +
            "; ".join(strengths) +
            "."
        )

    if concerns:

        reasoning += (
            " Concerns: " +
            "; ".join(concerns[:2]) +
            "."
        )

    return reasoning