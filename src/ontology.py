"""
Skill normalization and technology relationships.
"""

NORMALIZATION = {

    # LLM
    "large language models": "llm",
    "llms": "llm",

    # RAG
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",

    # Torch
    "torch": "pytorch",

    # Cloud
    "amazon web services": "aws",
    "google cloud platform": "gcp",

    # Databases
    "postgres": "postgresql",

    # Search
    "vector search": "embeddings",

    # Misc
    "sentence transformers": "embeddings",
}


RELATED_SKILLS = {

    # Vector Databases
    "faiss": {
        "milvus",
        "pinecone",
        "qdrant",
        "weaviate",
    },

    "milvus": {
        "faiss",
        "pinecone",
        "qdrant",
        "weaviate",
    },

    "pinecone": {
        "faiss",
        "milvus",
        "qdrant",
        "weaviate",
    },

    "qdrant": {
        "faiss",
        "milvus",
        "pinecone",
        "weaviate",
    },

    "weaviate": {
        "faiss",
        "milvus",
        "pinecone",
        "qdrant",
    },

    # Frameworks
    "langchain": {
        "llamaindex",
        "haystack",
    },

    "llamaindex": {
        "langchain",
        "haystack",
    },

    "haystack": {
        "langchain",
        "llamaindex",
    },

    # APIs
    "fastapi": {
        "flask",
        "django",
    },

    # RAG
    "rag": {
        "retrieval",
        "retrieval augmented generation",
    },
}