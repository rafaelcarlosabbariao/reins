# app/components/portfolio/resource_list.py
import reflex as rx
from app.state import AppState as State

def _row(r) -> rx.Component:
    return rx.card(
        rx.hstack(
            # Left: name + role/type/dept
            rx.vstack(
                rx.text(r["name"], weight="medium"),
                rx.text(
                    rx.fragment(
                        r["role"], " · ",
                        r["type"], " · ",
                        r["dept"]
                    ),
                    size="1",
                    color="gray",
                ),
                spacing="1",
                align="start",
                width="100%",
            ),

            rx.spacer(),

            # Right: utilization and progress bar + date range
            rx.vstack(
                rx.text(
                    rx.fragment(r["util"], "%"),
                    size="2",
                    weight="bold",
                ),
                # Use a progress component to avoid string concat for CSS width
                rx.progress(value=r["util"], max=100, width="160px"),
                rx.text(r["range"], size="1", color="gray"),
                spacing="1",
                align="end",
            ),

            align="center",
            width="100%",
            gap="3",
        ),
        padding="0.75rem",
        radius="xl",
        shadow="sm",
        width="100%",
        _hover={"boxShadow": "0 8px 18px rgba(0,0,0,0.08)"},
    )


def resource_list() -> rx.Component:
    """Allocated resources list. Uses rx.foreach over Var list."""
    return rx.card(
        rx.vstack(
            rx.text("Allocated Resources Detail", size="3", weight="bold"),

            rx.cond(
                State.has_selection,
                rx.vstack(
                    rx.foreach(State.sel_resources, lambda r: _row(r)),
                    spacing="2", 
                    width="100%",
                ),
                rx.box(),  # nothing if no selection
            ),

            spacing="3",
            width="100%",
            align="start",
        ),
        padding="0.75rem",
        radius="xl",
        shadow="sm",
        width="100%",
    )
