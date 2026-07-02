import json
from pathlib import Path

JOB_PROFILE_PATH = Path("outputs/job_profile.json")


def load_job_profile():
    """Load the parsed job profile."""

    with JOB_PROFILE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)