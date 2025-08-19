from __future__ import annotations
import reflex as rx
from app.state import AppState as State


def resources_by_department_chart() -> rx.Component:
    chart = rx.recharts.bar_chart(
        # grid, axes, tooltip, series
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),

        rx.recharts.x_axis(
            # ⬇️ axis label as a *positional* child
            rx.recharts.label(
                value="Department",
                position="insideBottom",
                offset=-5,
            ),
            data_key="department",
            interval=0,
            height=50,
        ),

        rx.recharts.y_axis(
            # ⬇️ axis label as a *positional* child
            rx.recharts.label(
                value="Hours",
                angle=-90,
                position="insideLeft",
                offset=10,
            ),
        ),

        rx.recharts.tooltip(),

        rx.recharts.bar(
            data_key="hours",
            fill="#3B82F6",
            radius=[6, 6, 0, 0],
        ),

        data=State.selected_department_chart_data,
        width="100%",
        height=300,
    )

    content = rx.cond(
        State.has_selected_department_data,
        chart,
        rx.center(
            rx.text("No data for this trial.", color="#64748B"),
            height="260px",
        ),
    )

    return rx.card(
        rx.vstack(
            rx.text("Hours by Department", weight="bold", color="black"),
            rx.box(height="1px", width="100%", bg="#E5E7EB"),
            content,
            spacing="3",
            width="100%",
            align="start",
        ),
        padding="16px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        width="100%",
    )
