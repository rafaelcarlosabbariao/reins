from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def _legend_row(item) -> rx.Component:
    # item is a Var with keys: label, pct, color
    return rx.hstack(
        rx.box(width="10px", height="10px", border_radius="50%", style={"background": item["color"]}),
        rx.text(item["label"], size="2", color="#0F172A"),
        rx.spacer(),
        rx.hstack(
            rx.text(item["pct"], size="2", color="#0F172A"),
            rx.text("%", size="2", color="#0F172A"),
            spacing="1",
            align="center",
        ),
        spacing="2",
        align="center",
        width="100%",
    )


def functional_area_pie() -> rx.Component:
    pie = rx.box(
        rx.box(
            # inner hole for donut effect
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
            style={"background": State.selected_functional_pie_bg},
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        width="100%",
        padding_y="10px",
    )

    legend = rx.vstack(
        rx.foreach(State.selected_functional_breakdown_colored, _legend_row),
        spacing="2",
        width="100%",
    )

    return rx.card(
        rx.vstack(
            rx.text("Functional Area Distribution", weight="bold", color="black"),
            rx.box(height="1px", width="100%", bg="#E5E7EB"),
            rx.hstack(
                pie,
                legend,
                spacing="6",
                align="center",
                width="100%",
                wrap="wrap",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="16px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
