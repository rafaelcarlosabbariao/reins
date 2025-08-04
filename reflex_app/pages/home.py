# reflex_app/pages/home.py

import reflex as rx
from reflex_app.components.hero import Hero
from reflex_app.components.about import AboutSection
from reflex_app.components.pipeline import PipelineSection
from reflex_app.components.focus_grid import FocusGrid
from reflex_app.components.footer import Footer

def HomePage():
    return rx.vstack(
        # Hero banner with CTAs
        Hero(),
        # About section (mission + features)
        rx.box(
            id="about",
            children=AboutSection(),
            padding="4rem 2rem",
            bg="white",
        ),
        # Pipeline section (programs by phase)
        rx.box(
            id="pipeline",
            children=PipelineSection(),
            padding="4rem 2rem",
            bg="#f8f9fa",
        ),
        # Areas of focus grid (functions)
        rx.box(
            id="focus",
            children=FocusGrid(),
            padding="4rem 2rem",
            bg="white",
        ),
        # Footer links
        Footer(),
        spacing="0",
    )
