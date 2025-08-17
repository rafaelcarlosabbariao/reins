import reflex as rx
from app.state import AppState as State
from .trial_card import trial_card

def trial_list() -> rx.Component:
    # Build rows in Python to avoid Var condition errors
    # rows = [trial_card(t) for t in State.trials]

    # -> State.trials is a Reflex var so can't iterate with Python list comprehension

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Clinical Trials", size="3", weight="bold"),
                align="center", width="100%",
            ),
            rx.input(placeholder="Search trials...", width="100%"),
            # rx.vstack(*rows, spacing="3", width="100%"),
            rx.vstack(
                rx.foreach(State.trials, lambda it: trial_card(it)),
                spacing="3",
                width="100%",
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        padding="0.75rem",
        radius="xl",
        shadow="sm",
        width="100%",
        height="36rem",
        overflow_y="auto",
    )
