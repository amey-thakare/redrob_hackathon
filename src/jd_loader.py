from pathlib import Path


def load_job_description():
    """
    Load the hackathon Job Description.
    """

    possible_files = [
        "data/job_description.txt",
        "data/job_description.md",
        "data/job_description.docx",
    ]

    for file in possible_files:

        path = Path(file)

        if path.exists():

            # txt / md
            if path.suffix in [".txt", ".md"]:
                return path.read_text(
                    encoding="utf-8"
                )

    raise FileNotFoundError(
        "Job description not found."
    )


from pathlib import Path

def load_job_description():
    return Path("data/job_description.txt").read_text(
        encoding="utf-8"
    )