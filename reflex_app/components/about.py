# reflex_app/components/about.py

import reflex as rx

def AboutSection():
    return rx.responsive_hstack(
        # left column: mission + icons
        rx.vstack(
            rx.heading("About REINS", size="2xl", color="gray.800"),
            rx.text(
                "Unified data foundation for CD&O resource management.", 
                size="md", 
                color="gray.600"
            ),
            rx.hstack(
                rx.vstack(rx.icon(name="FaUserCheck", font_size="2xl"), rx.text("Named Resource Tracking")),
                rx.vstack(rx.icon(name="FaChartLine", font_size="2xl"), rx.text("Demand Harmonization")),
                rx.vstack(rx.icon(name="FaCogs", font_size="2xl"), rx.text("FSP Strategy")),
                spacing="2rem",
            ),
            spacing="1rem",
            flex=1,
        ),
        # right column: feature accordions
        rx.accordion(
            rx.accordion_item(
                rx.accordion_button("Unified Data Foundation"),
                rx.accordion_panel("Centralized CD&O resource data warehouse.")
            ),
            rx.accordion_item(
                rx.accordion_button("AI-powered Insights"),
                rx.accordion_panel("Intelligent alerts & automated summaries.")
            ),
            rx.accordion_item(
                rx.accordion_button("Scenario Modeling"),
                rx.accordion_panel("What-if analyses for FTE, phases, and vendors.")
            ),
            flex=1,
        ),
        spacing="4rem",
        wrap="wrap",
        spacing_responsive=["2rem","4rem"],
    )
