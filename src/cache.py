from functools import lru_cache


@lru_cache(maxsize=None)
def cached_encode(model, text):
    return model.encode(
        text,
        normalize_embeddings=True
    )