CAREER_KEYWORDS = {
    "retrieval",
    "ranking",
    "reranking",
    "semantic search",
    "hybrid search",
    "vector search",
    "recommendation",
    "recommendation system",
    "embedding",
    "embeddings",
    "pinecone",
    "faiss",
    "qdrant",
    "milvus",
    "weaviate",
    "pgvector",
    "llm",
    "langchain",
    "llamaindex",
    "rag",
    "production",
    "deployed",
    "deployment",
    "pipeline",
    "distributed",
    "microservice",
    "serving",
    "real-time",
    "latency",
    "offline evaluation",
    "online evaluation",
    "ndcg",
    "mrr",
    "map",
    "precision@k",
    "recall@k",
    "a/b test",
    "relevance",
}

JOB_SKILLS = {
    "Python",
    "LLM",
    "Transformers",
    "LangChain",
    "RAG",
    "Embeddings",
    "Pinecone",
    "Qdrant",
    "FAISS",
    "Elasticsearch",
    "Vector Database",
    "Hybrid Search",
    "Retrieval",
    "Ranking",
    "Reranking",
    "LlamaIndex",
    "Haystack",
    "Sentence Transformers",
    "pgvector",
    "Milvus",
    "Weaviate",
    "FastAPI",
    "PyTorch",
}
SEARCH_TITLES = {
    "search",
    "retrieval",
    "ranking",
    "relevance",
}

AI_TITLES = {
    "machine learning",
    "ml engineer",
    "ai engineer",
    "applied scientist",
    "nlp",
    "staff machine learning",
    "senior machine learning",
    "llm engineer",
    "genai engineer",
    "generative ai",
    "foundation model",
}

AI_INDUSTRIES = {
    "AI/ML",
    "AI Services",
    "Conversational AI",
    "HealthTech AI",
    "Voice AI",
}

def compute_job_match(candidate):

    score = 0.0

    profile = candidate["profile"]

    # -----------------------
    # Skill overlap
    # -----------------------

    skills = {
    s["name"].lower()
    for s in candidate["skills"]
}

    job_skills = {
    skill.lower()
    for skill in JOB_SKILLS
}

    overlap = len(
    skills & job_skills
)

    score += min(overlap, 10) * 0.05

    # -----------------------
    # Current title
    # -----------------------

    title = profile["current_title"].lower()

    if any(word in title for word in SEARCH_TITLES):
        score += 0.25

    elif any(word in title for word in AI_TITLES):
        score += 0.18

    # -----------------------
    # Industry
    # -----------------------

    industry = profile.get(
    "current_industry",
    ""
)

    if industry in AI_INDUSTRIES:
        score += 0.15

    elif (
    "software" in industry.lower()
    or "technology" in industry.lower()
):
        score += 0.08
        

    # -----------------------
    # Experience
    # -----------------------

    exp = profile["years_of_experience"]

    if 5 <= exp <= 9:
        score += 0.20

    elif 4 <= exp <= 10:
        score += 0.10

    # -----------------------
    # Career history
    # -----------------------

    text = ""

    for job in candidate["career_history"]:

        text += job.get("title", "") + " "
        text += job.get("description", "") + " "

    text = text.lower()

    keywords = [
        "retrieval",
        "ranking",
        "reranking",
        "semantic search",
        "hybrid search",
        "vector search",
        "recommendation",
        "recommendation system",
        "embedding",
        "embeddings",
        "pinecone",
        "faiss",
        "qdrant",
        "milvus",
        "weaviate",
        "pgvector",
        "llm",
        "langchain",
        "llamaindex",
        "rag",
        "production",
        "deployed",
        "deployment",
        "pipeline",
        "distributed",
        "microservice",
        "serving",
        "real-time",
        "latency",
        "offline evaluation",
        "online evaluation",
        "ndcg",
        "mrr",
        "map",
        "precision@k",
        "recall@k",
        "a/b test",
        "relevance"
    ]

    matches = sum(
        keyword in text
        for keyword in keywords
    )

    score += min(matches, 8) * 0.04

    return min(score, 1.0)