# reflex_app/components/pipeline.py

import reflex as rx

def PipelineSection():
    phases = ["Discovery", "Phase I", "Phase II", "Phase III", "Launch"]
    return rx.vstack(
        rx.heading("Pipeline of Programs by Phase", size="xl", color="gray.800"),
        rx.hstack(
            *[
                rx.box(
                    rx.text(phase, font_size="lg", font_weight="semibold"),
                    rx.text("0 Programs", font_size="md", color="gray.600"),
                    rx.button("View details", size="sm", on_click=lambda p=phase: None),
                    padding="1rem",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="md",
                    min_w="140px",
                )
                for phase in phases
            ],
            overflow_x="auto",
            spacing="1rem",
            py="1rem",
        ),
    )
