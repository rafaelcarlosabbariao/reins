import reflex as rx

def view() -> rx.Component:
    return rx.vstack(
        rx.heading("Resources", size="8"),
        rx.text("Named resource list, skill matrix, and heatmap will render here."),
        rx.card(rx.text("Heatmap placeholder"), height="22rem"),
        spacing="4",
        width="100%",
    )