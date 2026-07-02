def build_resume_text(candidate):
    """
    Convert a structured candidate profile into a single
    semantic document for embedding.
    """

    profile = candidate["profile"]

    sections = []

    # Current role
    sections.append(
        f"Current Title: {profile['current_title']}"
    )

    sections.append(
        f"Headline: {profile.get('headline', '')}"
    )

    sections.append(
        f"Summary: {profile.get('summary', '')}"
    )

    sections.append(
        f"Experience: {profile['years_of_experience']} years"
    )

    sections.append(
        f"Industry: {profile['current_industry']}"
    )

    # Skills
    skill_text = []

    for skill in candidate["skills"]:

        skill_text.append(
            f"{skill['name']} ({skill['proficiency']})"
        )

    sections.append(
        "Skills: " + ", ".join(skill_text)
    )

    # Career history
    history = []

    for job in candidate["career_history"]:

        history.append(
            f"""
Company: {job['company']}
Title: {job['title']}
Industry: {job['industry']}
Description:
{job['description']}
""".strip()
        )

    sections.append(
        "\n".join(history)
    )

    return "\n\n".join(sections)