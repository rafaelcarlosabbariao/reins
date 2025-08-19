import reflex as rx
from app.state import AppState as State

def _title_block() -> rx.Component:
    return rx.vstack(
        rx.heading("Resource Management", size="8"),
        rx.text(
            "Manage resources, capacity planning, and trial allocations",
            color="#64748B",
        ),
        spacing="2",
        align="start",
    )

def _primary_actions() -> rx.Component:
    return rx.hstack(
        rx.button(
            rx.hstack(rx.icon(tag="plus", size=16), rx.text("Add Position")),
            variant="soft",
            padding_x="14px",
            padding_y="10px",
            border_radius="12px",
        ),
        rx.button(
            rx.hstack(rx.icon(tag="plus", size=16), rx.text("Add Resource")),
            variant="solid",
            padding_x="14px",
            padding_y="10px",
            border_radius="12px",
        ),
        spacing="3",
        align="center",
    )

def _search_row() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(tag="search", size=18, color="gray.10"),
            rx.input(
                placeholder="Search resources and positions...",
                value=State.resources_search,
                on_change=State.set_resources_search_,
                size="3",
                width="100%",
            ),
            spacing="2",
            align="center",
        ),
        padding="10px",
        border="1px solid #E5E7EB",
        border_radius="10px",
        bg="white",
        width="100%",
    )

def _tabs_row() -> rx.Component:
    return rx.tabs.root(
        rx.tabs.list(
            [
                rx.tabs.trigger(
                    rx.hstack(
                        rx.text("Resources ("),
                        rx.text(State.total_resources),   # <-- state var, not lambda
                        rx.text(")"),
                        spacing="1",
                        align="center",
                    ),
                    value="resources",
                    on_click=lambda: State.set_resources_tab_("resources"),
                ),
            ],
            wrap="wrap",
            gap="6px",
        ),
        # Keep tabs uncontrolled; avoid on_value_change (not supported in your build)
        default_value="resources",
        activation_mode="automatic",
    )

def header() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            _title_block(),
            rx.spacer(),
            _primary_actions(),
            width="100%",
            align="center",
        ),
        _search_row(),
        _tabs_row(),
        spacing="4",
        width="100%",
    )
