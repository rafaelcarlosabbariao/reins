import reflex as rx
from app.state import AppState as State

def _bar(label: str, pct: int, color: str) -> rx.Component:
    pct_str = f"{pct}%"
    return rx.vstack(
        rx.hstack(rx.text(label, size="2"), rx.spacer(), rx.text(pct_str, size="2"), align="center", width="100%"),
        rx.box(
            rx.box(width=pct_str, height="8px", background=color, radius="full"),
            width="100%", height="8px", background="#F3F4F6", radius="full",
        ),
        spacing="1",
        width="100%",
        align="start",
    )

def utilization_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Resource Utilization", size="3", weight="bold"),
                align="center", width="100%",
            ),
            rx.hstack(
                rx.heading(f"{State.portfolio_avg_util}%", size="8"),
                rx.vstack(
                    rx.text("Overall Utilization", size="2", color="gray"),
                    rx.text("Optimal range", size="2", color="#059669"),
                    spacing="1",
                    align="start",
                ),
                spacing="4",
                align="center",
            ),
            _bar("FTE Resources", State.fte_pct, "#2563EB"),
            _bar("FSP/Contractors", State.fsp_pct, "#CBD5E1"),
            rx.hstack(
                rx.vstack(rx.heading(State.fte_pct // 5 * 1, size="5"), rx.text("FTE", size="2", color="gray")),
                rx.spacer(),
                rx.vstack(rx.heading(State.fsp_pct // 7 * 1, size="5"), rx.text("FSP", size="2", color="gray")),
                align="end", width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="1rem",
        radius="xl",
        shadow="sm",
        width="100%",
    )
