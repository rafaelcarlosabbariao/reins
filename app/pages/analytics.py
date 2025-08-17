import reflex as rx
from app.state import AppState as State
from app.components.analytics.kpi_card import kpi_card

def view() -> rx.Component:
    return rx.vstack(
        rx.heading("Analytics", size="8"),
        rx.grid(
            rx.foreach(State.kpi_pairs, lambda pair: kpi_card(pair[0], pair[1])),
            columns="4",
            gap="1rem",
            width="100%",
        ),
        rx.card(
            rx.text("Charts go here (e.g., Plotly)."),
            height="22rem",
        ),
        spacing="4",
        width="100%",
    )