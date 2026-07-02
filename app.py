import os
import tempfile
import subprocess

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Redrob Candidate Ranker",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Redrob AI Candidate Ranker")

uploaded = st.file_uploader(
    "Upload candidates.jsonl",
    type=["jsonl"]
)

if uploaded is not None:

    with tempfile.TemporaryDirectory() as tmp:

        input_path = os.path.join(
            tmp,
            "candidates.jsonl"
        )

        with open(input_path, "wb") as f:
            f.write(uploaded.read())

        output_path = os.path.join(
            tmp,
            "submission.csv"
        )

        with st.spinner("Ranking candidates..."):

            subprocess.run(
                [
                    "python3",
                    "rank.py",
                    "--candidates",
                    input_path,
                    "--out",
                    output_path
                ],
                check=True
            )

        df = pd.read_csv(output_path)

        st.success("Ranking complete!")

        st.dataframe(df)

        st.download_button(
            "Download Ranked CSV",
            df.to_csv(index=False),
            file_name="submission.csv",
            mime="text/csv"
        )