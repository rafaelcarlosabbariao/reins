# reflex_app/state/demand_state.py

import reflex as rx
import pandas as pd

class DemandState(rx.State):
    requests: list[dict] = []

    def load_data(self):
        df = pd.read_csv("data/processed/demand_requests.csv")
        self.requests = df.to_dict(orient="records")

    def approve_selected(self, ids: list[int]):
        # TODO: implement real approval logic
        approved = [r for r in self.requests if r["id"] in ids]
        print(f"Approved requests: {ids}")
