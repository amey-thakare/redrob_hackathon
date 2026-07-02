# Redrob Candidate Ranking System

## Overview

This project ranks candidates for the Redrob AI Engineer hiring challenge.

The ranking pipeline consists of three stages:

1. Rule-based feature engineering and weighted scoring.
2. Semantic reranking using Sentence Transformers.
3. CrossEncoder reranking of the top candidates.

The system generates a Top-100 ranked submission CSV with candidate-specific reasoning.

---

## Features

- Job description matching
- Title and seniority scoring
- Experience scoring
- AI / GenAI skill matching
- Skill quality scoring
- Product-company background scoring
- Retrieval and ranking system experience detection
- Production ML experience detection
- Recruiter engagement signals
- Honeypot candidate detection
- CrossEncoder reranking
- Candidate-specific reasoning generation

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python rank.py --candidates data/candidates.jsonl --out outputs/submission.csv
```

---

## Output

The generated CSV is:

```text
outputs/submission.csv
```

Columns:

- candidate_id
- rank
- score
- reasoning

---

## Performance

- Dataset size: 100,000 candidates
- CPU-only execution
- Stage 1 runtime: ~90 seconds
- Total runtime: Under 5 minutes
- No hosted LLM APIs used during ranking

---

## Models Used

- sentence-transformers/all-MiniLM-L6-v2
- cross-encoder/ms-marco-MiniLM-L-6-v2

---

## Repository Structure

```text
.
├── data/
├── outputs/
├── src/
├── rank.py
├── app.py
├── requirements.txt
├── submission_metadata.yaml
└── README.md
```

---

## Ranking Pipeline

### Stage 1
Rule-based candidate scoring using engineered features:
- Job match score
- AI skills
- Product engineering experience
- Ranking and retrieval experience
- Recruiter engagement
- Company quality
- Validator-based honeypot filtering

### Stage 2
Semantic similarity reranking using Sentence Transformers for the top candidates.

### Stage 3
CrossEncoder reranking using `cross-encoder/ms-marco-MiniLM-L-6-v2` to produce the final ranking.

---

## AI Usage

ChatGPT was used for brainstorming, debugging, and code review.

The complete ranking pipeline, feature engineering, implementation, testing, and validation were developed and verified by the team.