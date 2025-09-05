import reflex as rx
from app.state import AppState as State
from app.components.resources.header import header
from app.components.resources.table import table
from app.components.resources.allocations_panel import allocations_panel

@rx.page(route="/resources", title="Resources", on_load=State.load_allocations)
def page() -> rx.Component:
    return rx.vstack(
        header(),
        table(),
        allocations_panel(),   # ⬅️ lives at page level, outside the table
        spacing="4",
        width="100%",
        padding="24px",
    )