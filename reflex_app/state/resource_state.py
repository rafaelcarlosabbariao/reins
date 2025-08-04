# reflex_app/state/resource_state.py

import reflex as rx
import pandas as pd

class ResourceState(rx.State):
    data: list[dict] = []

    def load_data(self):
        df = pd.read_csv("data/processed/resources.csv")
        self.data = df.to_dict(orient="records")

    @rx.var
    def total_resources(self) -> int:
        return len(self.data)
