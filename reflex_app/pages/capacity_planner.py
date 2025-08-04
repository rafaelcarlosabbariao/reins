# reflex_app/pages/capacity_planner.py

import reflex as rx

def CapacityPlannerPage():
    return rx.vstack(
        rx.heading("Capacity Planner", size="2xl", color="gray.800"),
        rx.text("Capacity heatmap placeholder", color="gray.600"),
    )
