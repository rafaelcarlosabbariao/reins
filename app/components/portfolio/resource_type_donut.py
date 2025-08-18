from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def _legend_dot(color: str) -> rx.Component:
    return rx.box(width="10px", height="10px", border_radius="50%", bg=color)


def resource_type_donut() -> rx.Component:
    """Donut card: FTE vs FSP/Contractor for the selected trial."""
    donut = rx.box(
        # outer ring painted by a conic-gradient
        rx.box(
            # inner hole
            rx.box(
                position="absolute",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width="56%",
                height="56%",
                border_radius="50%",
                bg="white",
            ),
            position="relative",
            width="220px",
            height="220px",
            border_radius="50%",
            style={"background": State.selected_type_donut_bg},
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        width="100%",
        padding_y="10px",
    )

    legend = rx.hstack(
        rx.hstack(_legend_dot("#3B82F6"), rx.text(rx.text.strong("FTE:"), " ", rx.text(State.selected_fte_pct, " %")), spacing="2", align="center"),
        rx.hstack(_legend_dot("#10B981"), rx.text(rx.text.strong("FSP:"), " ", rx.text(State.selected_fsp_pct, " %")), spacing="2", align="center"),
        spacing="6",
        justify="center",
        width="100%",
    )

    return rx.card(
        rx.vstack(
            rx.text("Resource Type Distribution", weight="bold", color="black"),
            rx.box(height="1px", width="100%", bg="#E5E7EB"),
            donut,            legend,
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="16px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
