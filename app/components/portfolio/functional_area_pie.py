# app/components/portfolio/functional_area_pie.py
from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def functional_area_pie() -> rx.Component:
    """Donut: Functional Area (Role) distribution by weighted hours for selected trial."""
    pie = rx.recharts.pie_chart(
        rx.recharts.tooltip(),
        # rx.recharts.legend(),
        rx.recharts.pie(
            # one Cell per role, colored from state
            rx.foreach(
                State.selected_functional_breakdown_colored,
                lambda d: rx.recharts.cell(fill=d["color"])
            ),
            data=State.selected_functional_breakdown_colored,  # [{"label","hours","pct","color"}...]
            data_key="hours",
            name_key="label",
            inner_radius=70,    # donut look
            outer_radius=110,
            padding_angle=2,
            label=True,         # show % labels on slices
        ),
        width="100%",
        height=300,
    )

    content = rx.cond(
        (State.selected_allocated_resources_count > 0),
        pie,
        rx.center(rx.text("No data for this trial.", color="#64748B"), height="260px"),
    )

    return rx.card(
        rx.vstack(
            rx.text("Functional Area Distribution", weight="bold", color="black"),
            rx.box(height="1px", width="100%", bg="#E5E7EB"),
            content,
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="16px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
