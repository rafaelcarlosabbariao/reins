import reflex as rx

def view() -> rx.Component:
    return rx.vstack(
        rx.heading("Timeline", size="8"),
        rx.text("Study timeline and milestones."),
        rx.card(rx.text("Timeline placeholder"), height="22rem"),
        spacing="4",
        width="100%",
    )