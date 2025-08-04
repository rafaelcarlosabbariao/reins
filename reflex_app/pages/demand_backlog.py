# reflex_app/pages/demand_backlog.py

import reflex as rx
from reflex_app.state.demand_state import DemandState

def DemandBacklogPage():
    return rx.vstack(
        rx.heading("Demand Backlog", size="2xl", color="gray.800"),
        rx.table(
            columns=["id", "study_name", "requested_fte", "status"],
            data=lambda: DemandState.requests,
            sortable=True,
            filterable=True,
            pagination=True,
        ),
        rx.button("Approve Selected", on_click=lambda: DemandState.approve_selected([1, 2]), size="md"),
    )
