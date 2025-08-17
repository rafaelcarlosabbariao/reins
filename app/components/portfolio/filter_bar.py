import reflex as rx
from app.state import AppState as State

def _select(label: str, options: list[str], value: str, on_change) -> rx.Component:
    return rx.hstack(
        rx.text(label, size="2", color="gray"),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            width="12rem",
        ),
        spacing="2",
        align="center",
    )

def filter_bar() -> rx.Component:
    return rx.hstack(
        _select("Status", State.filter_status, State.selected_status, State.set_selected_status),
        _select("Phases", State.filter_phase, State.selected_phase, State.set_selected_phase),
        _select("Priority", State.filter_priority, State.selected_priority, State.set_selected_priority),
        _select("Areas", State.filter_area, State.selected_area, State.set_selected_area),
        _select("Departments", State.filter_dept, State.selected_dept, State.set_selected_dept),
        spacing="3",
        wrap="wrap",
        width="100%",
    )
