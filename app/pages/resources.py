import reflex as rx
from app.components.resources.header import header

def view() -> rx.Component:
    return rx.vstack(
        header(),
        rx.text("Named resource list, skill matrix, and heatmap will render here."),
        rx.card(rx.text("Heatmap placeholder"), height="22rem"),
        spacing="4",
        width="100%",
        max_width="1600px",
        margin_x="auto",
    )