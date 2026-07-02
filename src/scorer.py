from src.validator import (
    impossible_profile,
    pure_service_background,
    job_hopper,
    inactive_candidate,
    title_skill_mismatch,
    suspicious_career_history
)
from src.validator import bad_title
from src.feature_engineering import extract_features
# Base weights for feature scores
BASE_WEIGHTS = {

    # Core Matching
    "job_match_score": 0.20,
    "title_score": 0.08,
    "experience_score": 0.08,
    "seniority_score": 0.05,

    # Skills
    "ai_skill_score": 0.13,
    "skill_quality_score": 0.06,
    "bonus_score": 0.03,
    "rare_skill_score": 0.03,

    # Product Engineering
    "product_background_score": 0.08,
    "ranking_system_score": 0.10,
    "product_mindset_score": 0.06,
    "evaluation_framework_score": 0.08,
    "production_system_score": 0.10,

    # Recruiter Signals
    "industry_score": 0.03,
    "open_to_work": 0.02,
    "notice_score": 0.03,
    "response_score": 0.04,
    "github_score": 0.02,
    "saved_score": 0.02,
    "search_score": 0.01,
    "company_size_score": 0.02,

    # Honeypot
    "honeypot_penalty": -0.30,
}
# Bonus rules: (condition_function, bonus_points, description)
BONUS_RULES = [
    (lambda f: f["rare_skill_score"] > 0.6, 0.03, "Strong GenAI profile"),
    (lambda f: f["seniority_score"] > 0.9, 0.02, "Senior candidate"),
    (lambda f: f["response_score"] > 0.8, 0.03, "Recruiters like this candidate"),
    (lambda f: f["github_score"] > 0.5, 0.02, "Active GitHub"),
    (lambda f: 0.8 <= f["experience_score"] <= 1, 0.02, "Good experience sweet spot"),
    (lambda f: f["industry_score"] == 1, 0.02, "AI-first industry"),
    (lambda f: f["saved_score"] > 0.3, 0.02, "High demand candidate"),
    (lambda f: f["search_score"] > 0.3, 0.02, "Highly searchable profile"),
    (
        lambda f: f["seniority_score"] > 0.8 and f["rare_skill_score"] > 0.6,
        0.03,
        "Senior + GenAI expert",
    ),
    (
        lambda f: f["response_score"] > 0.8 and f["github_score"] > 0.5,
        0.03,
        "Strong recruiter engagement + GitHub",
    ),

    
   
]

# Penalty rules: (condition_function, penalty_points, description)
PENALTY_RULES = [
   
    (lambda f: f["notice_score"] < 0.4, 0.04, "Long notice period"),
    (lambda f: f["ai_skill_score"] < 0.2, 0.05, "Very few AI skills"),
    (lambda f: f["response_score"] < 0.2, 0.05, "Low recruiter engagement"),
 
    (lambda f: f["experience_score"] < 0.5,0.04,"Experience outside sweet spot"),
]


def _compute_base_score(features):

    score = 0.0

    for feature, weight in BASE_WEIGHTS.items():

        score += weight * features.get(feature, 0)

    return score


def _apply_bonuses(score, features):
    """Apply bonus rules to score."""
    for condition, bonus, _ in BONUS_RULES:
        if condition(features):
            score += bonus
    return score


def _apply_penalties(score, features):
    """Apply penalty rules to score."""
    for condition, penalty, _ in PENALTY_RULES:
        if condition(features):
            score -= penalty
    return score


def _apply_soft_penalties(score, candidate):

    if title_skill_mismatch(candidate):
        score -= 0.25

    if suspicious_career_history(candidate):
        score -= 0.20

    if job_hopper(candidate):
        score -= 0.08

    if pure_service_background(candidate):
        score -= 0.10

    return score

def compute_score(candidate):

    # Hard filters
    if impossible_profile(candidate):
        return 0.0

    if bad_title(candidate):
        return 0.0

    if inactive_candidate(candidate):
        return 0.0

    features = extract_features(candidate)

    score = _compute_base_score(features)

    score = _apply_soft_penalties(
        score,
        candidate,
    )

    score = _apply_bonuses(
        score,
        features,
    )

    score = _apply_penalties(
        score,
        features,
    )
    
    return round(
        max(0.0, min(score, 1.0)),
        4,
    )

 
    
