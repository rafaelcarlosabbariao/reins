import reflex as rx
from app.components.resources.header import header
from app.components.resources.table import table

@rx.page(route="/resources", title="Resources")
def page() -> rx.Component:
    return rx.vstack(
        header(),
        table(),
        spacing="4",
        width="100%",
        padding="24px",
        margin_x="auto",
    )