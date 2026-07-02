from sentence_transformers import CrossEncoder

MODEL = CrossEncoder("BAAI/bge-reranker-base")


def rerank(job_document, candidates):

    pairs = [
        (job_document, c["document"])
        for c in candidates
    ]

    scores = MODEL.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate["rerank_score"] = float(score)

    candidates.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return candidates