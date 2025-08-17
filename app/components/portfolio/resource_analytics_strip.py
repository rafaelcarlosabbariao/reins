import reflex as rx
from app.state import AppState as State

def analytics_strip() -> rx.Component:
    return rx.cond(
        State.has_selection,
        rx.card(
            rx.hstack(
                rx.badge(State.selected_trial["id"], size="2"),
                rx.badge(State.selected_trial["phase"], size="2", background="#E8F5E9", color="#147D2B"),
                rx.badge(State.selected_trial["area"], size="2", background="#EEF2FF", color="#3730A3"),
                rx.spacer(),

                rx.vstack(
                    rx.text("Allocated Resources", size="1", color="gray"),
                    rx.heading(State.sel_alloc["allocated_resources"], size="6"),
                    spacing="1",
                    align="start",
                ),
                rx.vstack(
                    rx.text("Weekly Hours", size="1", color="gray"),
                    rx.heading(State.sel_weekly_hours_label, size="6"),
                    spacing="1",
                    align="start",
                ),
                rx.vstack(
                    rx.text("Avg Utilization", size="1", color="gray"),
                    rx.heading(State.sel_avg_util_label, size="6", color="#7C3AED"),
                    spacing="1",
                    align="start",
                ),
                rx.vstack(
                    rx.text("Over-allocated", size="1", color="gray"),
                    rx.heading(State.sel_over_alloc_label, size="6"),
                    spacing="1",
                    align="start",
                ),

                align="center",
                width="100%",
                wrap="wrap",
                gap="5",
            ),
            padding="0.75rem",
            radius="xl",
            shadow="sm",
            width="100%",
        ),
        rx.box(),
    )
