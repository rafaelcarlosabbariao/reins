# reflex_app/pages/scenarios.py

import reflex as rx

def ScenariosPage():
    return rx.vstack(
        rx.heading("Scenario Modeling", size="2xl", color="gray.800"),
        rx.text("Scenario sliders & outcomes placeholder", color="gray.600"),
    )
