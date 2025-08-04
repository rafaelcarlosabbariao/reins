# reflex_app/components/app_shell.py

import reflex as rx
from reflex_app.components.footer import Footer

def AppShell(children):
    return rx.vstack(
        # Header
        rx.hstack(
            rx.image(src="/assets/reins-logo.png", alt="REINS Logo", height="50px"),
            rx.link("Home", href="/"),
            rx.link("Portfolio", href="/portfolio"),
            rx.link("Capacity", href="/capacity"),
            rx.link("Demand", href="/demand"),
            rx.link("Scenarios", href="/scenarios"),
            justify="space-between",
            align="center",
            padding="1rem 2rem",
            bg="rgb(0,53,128)",
            color="white",
        ),
        # Main content
        rx.box(children, flex=1),
        # Footer
        Footer(),
    )
