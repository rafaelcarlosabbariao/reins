# app/components/portfolio/resource_summary.py
from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def _pill(text: rx.Var | str, fg: str = "#475569", bg: str = "#F1F5F9") -> rx.Component:
    return rx.box(
        rx.text(text, size="2", weight="regular", color=fg),
        padding_x="8px",
        padding_y="4px",
        border_radius="9999px",
        style={"background": bg},
    )


def _metric(value_comp: rx.Component, label: str) -> rx.Component:
    """Stack for a metric: big value (already colored) + gray label."""
    return rx.vstack(
        value_comp,
        rx.text(label, size="2", color="#64748B"),
        spacing="1",
        align="center",
    )


def _value_with_suffix(value_var: rx.Var | str, suffix: str, color: str) -> rx.Component:
    """Render a big colored value with a small suffix next to it (e.g., '20' + 'h')."""
    return rx.hstack(
        rx.text(value_var, size="5", weight="bold", color=color),
        rx.text(suffix,     size="5", weight="bold", color=color),
        spacing="1",
        align="center",
    )


def resource_summary_strip() -> rx.Component:
    """Summary header + four KPIs for the selected trial (reactive-safe)."""

    # Header title: either plain label or "Resource Analytics: <trial title>"
    header_title = rx.cond(
        (State.selected_trial_id == None),
        rx.text("Resource Analytics", weight="bold", color="#64748B"),
        rx.hstack(
            rx.text("Resource Analytics: ", weight="bold", color="#64748B"),
            # Use separate text node for the reactive title (no string + Var)
            rx.text(State.selected_trial["title"], weight="bold"),
            align="center",
            spacing="1",
        ),
    )

    return rx.card(
        rx.vstack(
            # Header row
            rx.hstack(
                rx.hstack(
                    rx.icon(tag="users", size=18, color="#2563EB"),
                    header_title,
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                align="center",
                width="100%",
            ),

            # Meta pills under the title
            rx.hstack(
                _pill(State.selected_protocol),
                _pill(State.selected_phase),
                _pill(State.selected_area),
                spacing="2",
                wrap="wrap",
            ),

            # Divider
            rx.box(height="1px", width="100%", style={"background": "#E2E8F0"}),

            # KPI row (4 equal columns)
            rx.grid(
                _metric(
                    rx.text(State.selected_allocated_resources_count, size="5", weight="bold", color="#2563EB"),
                    "Allocated Resources",
                ),
                _metric(
                    _value_with_suffix(State.selected_weekly_hours, "h", "#059669"),
                    "Weekly Hours",
                ),
                _metric(
                    _value_with_suffix(State.selected_avg_util, "%", "#7C3AED"),
                    "Avg Utilization",
                ),
                _metric(
                    rx.text(State.selected_overallocated, size="5", weight="bold", color="#059669"),
                    "Over-allocated",
                ),
                columns=rx.breakpoints({"base": "2", "md": "4"}),
                spacing="4",
                width="100%",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        padding="18px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
