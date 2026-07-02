from src.feature_engineering import extract_features


def feature_vector(candidate):

    f = extract_features(candidate)

    return [

        f["job_match_score"],
        f["title_score"],
        f["experience_score"],
        f["ai_skill_score"],
        f["skill_quality_score"],
        f["bonus_score"],
        f["semantic_score"],
        f["product_background_score"],
        f["ranking_system_score"],
        f["product_mindset_score"],
        f["evaluation_framework_score"],
        f["production_system_score"],
        f["industry_score"],
        f["open_to_work"],
        f["notice_score"],
        f["response_score"],
        f["github_score"],
        f["saved_score"],
        f["company_size_score"],
    ]