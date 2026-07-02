import numpy as np
from sentence_transformers import SentenceTransformer

from src.loader import load_candidates
from src.semantic_matcher import build_candidate_text

print("Loading model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Loading candidates...")

candidates = load_candidates(
    "data/candidates.jsonl"
)

texts = [
    build_candidate_text(c)
    for c in candidates
]

print(f"Encoding {len(texts)} candidates...")

embeddings = model.encode(
    texts,
    batch_size=256,
    normalize_embeddings=True,
    show_progress_bar=True
)

np.save(
    "data/candidate_embeddings.npy",
    embeddings
)

print("Done.")