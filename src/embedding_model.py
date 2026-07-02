from sentence_transformers import SentenceTransformer

_MODEL = None


def get_model():
    """
    Lazily load the embedding model so it is only loaded once.
    """

    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    return _MODEL


def embed(texts):
    """
    Embed one or more texts.
    """

    model = get_model()

    return model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )