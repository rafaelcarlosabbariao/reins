import reflex as rx
from app.state import AppState as State

def ratio_bar() -> rx.Component:
    # One split bar: left (FTE) / right (FSP)
    return rx.hstack(
        rx.box(height="8px", width=f"{State.fte_pct}%", background="#2563EB", radius="full"),
        rx.box(height="8px", width=f"{State.fsp_pct}%", background="#CBD5E1", radius="full"),
        width="100%",
        spacing="0",
        border_radius="9999px",
        overflow="hidden",
        border="1px solid #E5E7EB",
    )

def ratio_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text("RESOURCE RATIO", size="1", color="gray", letter_spacing="0.08em"),
            rx.hstack(
                rx.text("FTE vs FSP", size="2", color="black"),
                rx.spacer(),
                rx.text("60:40", weight="medium", color="blue"),
                align="center",
                width="100%",
            ),
            ratio_bar(),
            rx.hstack(
                rx.text("FTE 60%", size="1", color="gray"),
                rx.spacer(),
                rx.text("FSP 40%", size="1", color="gray"),
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        padding="0.75rem",
        radius="lg",
        shadow="sm",
        width="100%",
    )
