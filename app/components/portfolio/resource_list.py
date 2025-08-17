import reflex as rx
from app.state import AppState as State

def _row(r: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.text(r["name"][0], weight="bold", color="white"),
                    width="36px", height="36px", background="#CBD5E1",
                    display="grid", place_items="center", radius="full",
                ),
                rx.vstack(
                    rx.text(r["name"], weight="medium"),
                    rx.text(f'{r["role"]} · {r["type"]} · {r["dept"]}', size="1", color="gray"),
                    spacing="0.1rem", align="start",
                ),
                gap="0.75rem", align="center",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(f'{r["util"]}%', size="2", weight="bold"),
                rx.box(
                    rx.box(width=f'{r["util"]}%', height="6px", background="#2563EB", radius="full"),
                    width="120px", height="6px", background="#E5E7EB", radius="full",
                ),
                rx.text(r["range"], size="1", color="gray"),
                spacing="0.25rem", align="end",
            ),
            align="center", width="100%",
        ),
        padding="0.5rem", radius="xl", shadow="sm", width="100%",
    )

def resource_list() -> rx.Component:
    rows = rx.cond(
        State.has_selection,
        rx.box(),
        rx.vstack(*[ _row(r) for r in State.sel_alloc["resources"] ], spacing="2", width="100%"),
    )
    return rx.card(
        rx.vstack(
            rx.text("Allocated Resources Detail", size="3", weight="bold"),
            rows,
            spacing="3", width="100%", align="start",
        ),
        padding="0.75rem", radius="xl", shadow="sm", width="100%",
    )
