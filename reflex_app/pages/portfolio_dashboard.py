# reflex_app/pages/portfolio_dashboard.py

import reflex as rx
from reflex_app.state.resource_state import ResourceState

def PortfolioDashboardPage():
    return rx.vstack(
        rx.heading("Portfolio Dashboard", size="2xl", color="gray.800"),
        rx.hstack(
            # Example summary card
            rx.box(
                rx.text("Total Resources"),
                rx.text(lambda: str(ResourceState.total_resources)),
                padding="1rem",
                border="1px solid gray.200",
                border_radius="md",
            ),
            # Add more cards here...
            spacing="2rem",
        ),
        rx.text("Portfolio bar chart placeholder", color="gray.600"),
    )
