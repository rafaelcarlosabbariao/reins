# reflex_app/components/footer.py

import reflex as rx

def Footer():
    return rx.box(
        rx.hstack(
            rx.link("Support", href="#"),
            rx.link("Privacy", href="#"),
            rx.link("Terms", href="#"),
            rx.link("Contact IT", href="#"),
            spacing="2rem",
            justify="center",
            wrap="wrap",
        ),
        padding="2rem",
        bg="gray.100",
    )
