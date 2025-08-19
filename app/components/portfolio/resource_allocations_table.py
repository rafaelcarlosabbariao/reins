# app/components/portfolio/resource_allocations_table.py
from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def _type_chip(text: rx.Var, color_bg: str, color_fg: str) -> rx.Component:
    return rx.box(
        rx.text(text, size="1", weight="medium", color=color_fg),
        padding_x="8px",
        padding_y="4px",
        border_radius="9999px",
        bg=color_bg,
    )


def _row(item) -> rx.Component:
    """One resource row."""
    left = rx.hstack(
        rx.box(
            rx.icon(tag="user", size=18, color="#64748B"),
            width="36px", height="36px", border_radius="50%", bg="#F1F5F9",
            display="flex", align_items="center", justify_content="center",
        ),
        rx.vstack(
            rx.text(item["name"], weight="bold", color="#0F172A"),
            rx.hstack(
                rx.text(item["role"], size="1", color="#64748B"),
                rx.text("•", size="1", color="#CBD5E1"),
                rx.cond(
                    (item["type"] == "FTE"),
                    _type_chip("FTE", "#DBEAFE", "#1D4ED8"),
                    _type_chip(item["type"], "#DCFCE7", "#059669"),
                ),
                rx.text("•", size="1", color="#CBD5E1"),
                rx.text(item["department"], size="1", color="#64748B"),
                spacing="2",
                align="center",
                wrap="wrap",
            ),
            spacing="1",
            align="start",
        ),
        spacing="3",
        align="center",
        width="100%",
    )

    right = rx.vstack(
        rx.hstack(
            rx.text(item["allocation_pct"], weight="bold", color="#0F172A"),
            rx.text("%", weight="bold", color="#0F172A"),
            spacing="2",
            align="center",
        ),
        rx.text(item["weekly_hours"], "h/week", size="1", color="#334155"),
        rx.text(item["date_range"], size="1", color="#94A3B8"),
        spacing="1",
        align="end",
        min_width="120px",
    )

    return rx.box(
        rx.hstack(left, right, align="center", width="100%"),
        padding="14px",
        border_radius="12px",
        bg="white",
        box_shadow="0 6px 18px rgba(15,23,42,0.06)",
        border="1px solid #EEF2F7",
        width="100%",
    )


def resource_allocations_table() -> rx.Component:
    header = rx.hstack(
        rx.text("Allocated Resources Detail", weight="bold", color="black"),
        rx.spacer(),
        rx.text(State.selected_resources_count, " total", size="1", color="#64748B"),
        align="center",
        width="100%",
    )

    body = rx.cond(
        (State.selected_resources_count > 0),
        rx.vstack(
            rx.foreach(State.selected_resources_detail, _row),
            spacing="3",
            width="100%",
        ),
        rx.center(rx.text("No allocations for this trial.", color="#64748B"), height="120px"),
    )

    return rx.card(
        rx.vstack(
            header,
            rx.box(height="1px", width="100%", bg="#E5E7EB"),
            body,
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="16px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
