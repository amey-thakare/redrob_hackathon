def build_history_text(candidate):

    return " ".join(
        (
            job.get("title", "")
            + " "
            + job.get("description", "")
        )
        for job in candidate["career_history"]
    ).lower()
PRODUCT_COMPANIES = {
    # Global AI / Product
    "Google",
    "Amazon",
    "Microsoft",
    "Meta",
    "Apple",
    "Netflix",
    "Uber",
    "Airbnb",
    "LinkedIn",
    "Stripe",
    "Databricks",
    "OpenAI",
    "NVIDIA",
    "Anthropic",
    "Cohere",
    "Scale AI",
    "Perplexity",
    "Palantir",
    "Figma",
    "Notion",
    "Canva",
    "Atlassian",
    "GitHub",
    "MongoDB",
    "Redis",
    "Elastic",
    "Snowflake",

    # Indian Product
    "Flipkart",
    "PhonePe",
    "Swiggy",
    "Zomato",
    "Meesho",
    "Razorpay",
    "CRED",
    "Groww",
    "Dream11",
    "Freshworks",
    "BrowserStack",
    "Postman",
    "Myntra",
    "Ola",
    "Juspay",
}

SERVICE_COMPANIES = {
    "TCS",
    "Infosys",
    "Wipro",
    "Cognizant",
    "Capgemini",
    "Accenture",
    "HCL",
    "Tech Mahindra",
    "LTIMindtree",
    "Mphasis",
    "Persistent Systems",
}
RANKING_KEYWORDS = {
    "retrieval",
    "ranking",
    "reranking",
    "recommendation",
    "semantic search",
    "vector search",
    "vector database",
    "embedding",
    "embeddings",
    "pinecone",
    "faiss",
    "qdrant",
    "milvus",
    "weaviate",
    "pgvector",
    "elasticsearch",
    "opensearch",
    "hybrid search",
    "langchain",
    "llamaindex",
    "rag",
    "llm",
    "ann",
}
PRODUCT_KEYWORDS = {
    "production",
    "deployed",
    "deployment",
    "scale",
    "scalable",
    "real-time",
    "latency",
    "pipeline",
    "microservice",
    "distributed",
    "serving",
    "online inference",
    "platform",
    "customer",
    "product",
    "user impact",
}
EVALUATION_KEYWORDS = {
    "ndcg",
    "mrr",
    "map",
    "precision",
    "recall",
    "offline evaluation",
    "online evaluation",
    "a/b",
    "ab test",
    "precision@k",
    "recall@k",
    "ranking metrics",
    "evaluation framework",
}
PRODUCTION_KEYWORDS = {
    "production",
    "deployment",
    "deployed",
    "docker",
    "kubernetes",
    "airflow",
    "spark",
    "streaming",
    "mlops",
    "pipeline",
    "microservice",
    "distributed",
    "real-time",
    "latency",
    "serving",
    "online inference",
    "high availability",
    "platform",
    "scalable",
}

def get_product_background_score(candidate):

    score = 0

    for job in candidate["career_history"]:

        company = job.get("company", "")

        industry = job.get("industry", "").lower()

        if company in PRODUCT_COMPANIES:
            score += 2

        elif company in SERVICE_COMPANIES:
            score -= 1

        if any(
            keyword in industry
            for keyword in (
                "ai",
                "software",
                "internet",
                "tech",
                "product",
            )
        ):
            score += 1

    return min(max(score, 0) / 8, 1.0)

def ranking_system_score(candidate):

    score = 0

    text = build_history_text(candidate)

    score += sum(
        keyword in text
        for keyword in RANKING_KEYWORDS
    )

    if (
        "rag" in text
        and (
            "faiss" in text
            or "pinecone" in text
            or "qdrant" in text
            or "weaviate" in text
            or "milvus" in text
        )
    ):
        score += 3

    if (
        "retrieval" in text
        and "ranking" in text
    ):
        score += 2

    if (
        "recommendation" in text
        and (
            "ndcg" in text
            or "mrr" in text
        )
    ):
        score += 2

    return min(score / 15, 1.0)


def product_mindset_score(candidate):

    profile = candidate["profile"]

    text = " ".join([
        profile.get("headline", ""),
        profile.get("summary", ""),
        *[
            job.get("title", "") + " " + job.get("description", "")
            for job in candidate["career_history"]
        ]
    ]).lower()

    score = sum(
        keyword in text
        for keyword in PRODUCT_KEYWORDS
    )

    if (
        "production" in text
        and "pipeline" in text
    ):
        score += 2

    if (
        "real-time" in text
        and "latency" in text
    ):
        score += 2

    if (
        "customer" in text
        or "user impact" in text
    ):
        score += 2

    if (
        "platform" in text
        and "scale" in text
    ):
        score += 2

    return min(score / 12, 1.0)
def evaluation_framework_score(candidate):

    text = " ".join(
        job.get("title", "") + " " + job.get("description", "")
        for job in candidate["career_history"]
    ).lower()

    score = sum(
        keyword in text
        for keyword in EVALUATION_KEYWORDS
    )

    if (
        "ndcg" in text
        and "mrr" in text
    ):
        score += 2

    if (
        "offline evaluation" in text
        and "online evaluation" in text
    ):
        score += 2

    if (
        "a/b" in text
        or "ab test" in text
    ):
        score += 2

    return min(score / 10, 1.0)

def production_system_score(candidate):

    text = " ".join(
        job.get("title", "") + " " + job.get("description", "")
        for job in candidate["career_history"]
    ).lower()

    score = sum(
        keyword in text
        for keyword in PRODUCTION_KEYWORDS
    )

    if (
        "docker" in text
        and "kubernetes" in text
    ):
        score += 3

    if (
        "mlops" in text
        and "airflow" in text
    ):
        score += 3

    if (
        "real-time" in text
        and "latency" in text
    ):
        score += 2

    if (
        "distributed" in text
        and "microservice" in text
    ):
        score += 2

    if (
        "pipeline" in text
        and "deployment" in text
    ):
        score += 2

    return min(score / 15, 1.0)

    