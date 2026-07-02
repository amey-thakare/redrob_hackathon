from pathlib import Path

SKILLS_FILE = Path(__file__).parent.parent / "data" / "skills.txt"

with open(SKILLS_FILE, "r") as f:
    SKILLS = [line.strip() for line in f if line.strip()]

def extract_skills(text):
    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found