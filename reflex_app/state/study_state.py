# reflex_app/state/study_state.py

import reflex as rx
import pandas as pd

class StudyState(rx.State):
    studies: list[dict] = []
    portfolios: list[dict] = []

    def load_data(self):
        df = pd.read_csv("data/processed/studies.csv")
        self.studies = df.to_dict(orient="records")
        pf_df = pd.read_csv("data/processed/portfolios.csv")
        self.portfolios = pf_df.to_dict(orient="records")
