from __future__ import annotations
import reflex as rx
from app.state import AppState as State

def resource_type_pie() -> rx.Component:
    # Recharts data: two slices from your State
    data = [
        {"name": "FTE", "value": State.selected_type_counts["fte"]},
        {"name": "FSP / Contractor", "value": State.selected_type_counts["fsp"]},
    ]

    chart = rx.recharts.pie_chart(
        rx.recharts.tooltip(),
        rx.recharts.legend(),
        rx.recharts.pie(
            # Colors for each slice (order matches `data` above)
            rx.recharts.cell(fill="#3B82F6"),   # FTE (blue)
            rx.recharts.cell(fill="#10B981"),   # FSP/Contractor (green)

            data=data,
            data_key="value",
            name_key="name",
            inner_radius=70,     # donut look
            outer_radius=110,
            padding_angle=2,
            label=True,          # show % labels on slices
        ),
        width="100%",
        height=300,
    )

    content = rx.cond(
        (State.selected_allocated_resources_count > 0),
        chart,
        rx.center(rx.text("No data for this trial.", color="#64748B"), height="260px"),
    )

    return rx.card(
        rx.vstack(
            rx.text("Resource Type Distribution", weight="bold", color="black"),
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
