from datetime import datetime


def honeypot_penalty(candidate):
    """
    Returns a penalty between 0 and 1.
    0 = genuine candidate
    1 = obvious honeypot
    """

    penalty = 0.0

    profile = candidate.get("profile", {})
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])

    years = profile.get("years_of_experience", 0)

    # -----------------------------
    # Impossible skill proficiency
    # -----------------------------
    for skill in skills:

        proficiency = skill.get("proficiency", "").lower()
        duration = skill.get("duration_months", 0)

        if proficiency == "expert" and duration < 6:
            penalty += 0.40

        elif proficiency == "advanced" and duration < 3:
            penalty += 0.20

    # -----------------------------
    # Too many expert skills
    # -----------------------------
    expert_count = sum(
        1
        for s in skills
        if s.get("proficiency", "").lower() == "expert"
    )

    if expert_count >= 10:
        penalty += 0.50
    elif expert_count >= 7:
        penalty += 0.30

    # -----------------------------
    # Total skill duration impossible
    # -----------------------------
    total_months = sum(
        s.get("duration_months", 0)
        for s in skills
    )

    if years > 0:

        max_possible = years * 12 * 3

        if total_months > max_possible:
            penalty += 0.40

    # -----------------------------
    # Career starts after experience
    # -----------------------------
    current_year = datetime.now().year

    earliest = current_year

    for job in career:

        start = job.get("start_date", "")

        if len(start) >= 4:

            try:
                earliest = min(
                    earliest,
                    int(start[:4])
                )
            except:
                pass

    if earliest != current_year:

        actual_years = current_year - earliest

        if abs(actual_years - years) > 3:
            penalty += 0.40

    # -----------------------------
    # Unrealistic skill count
    # -----------------------------
    if len(skills) >= 35:
        penalty += 0.20

    elif len(skills) >= 45:
        penalty += 0.40

    return min(1.0, penalty)