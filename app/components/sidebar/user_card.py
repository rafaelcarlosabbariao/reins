import reflex as rx
from app.state import AppState as State

def user_card() -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.text(State.user_initials, weight="bold", color="white"),
                width="36px", height="36px",
                background="#059669",  # teal/green dot like your mock
                display="grid", place_items="center",
                radius="full",
            ),
            rx.vstack(
                rx.text(State.user_name, weight="medium", color="black"),
                rx.text(State.user_role, size="1", color="gray"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        padding="0.75rem",
        radius="lg",
        shadow="sm",
        width="100%",
    )
