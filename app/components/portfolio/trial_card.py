import reflex as rx
from app.state import AppState as State

def _status_badge(status: str) -> rx.Component:
    color_map = {
        "Ongoing": "#10B981",
        "Planning": "#3B82F6",
        "Paused": "#F59E0B",
    }
    return rx.badge(status, size="2", background="#ECFDF5", color=color_map.get(status, "#065F46"))

def _phase_badge(phase: str) -> rx.Component:
    return rx.badge(phase, size="2", background="#EEF2FF", color="#3730A3")

def trial_card(trial: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(trial["title"], weight="bold"),
                rx.spacer(),
                # action icons (placeholders)
                rx.link("↗", href=f"/portfolio?trial={trial['id']}"),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.hstack(
                rx.badge(trial["id"], size="2"),
                _phase_badge(trial["phase"]),
                _status_badge(trial["status"]),
                spacing="2",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="0.75rem",
        radius="xl",
        shadow="sm",
        width="100%",
        on_click=lambda: State.select_trial(trial["id"]),
        _hover={"boxShadow": "0 8px 18px rgba(0,0,0,0.08)", "cursor": "pointer"},
    )
