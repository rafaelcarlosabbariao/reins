import reflex as rx
from app.state import AppState as State

def _type_badge(label, color, bg) -> rx.Component:
    return rx.box(
        rx.text(label, size="2"),
        padding_x="10px",
        padding_y="2px",
        border_radius="9999px",
        bg=bg,             # Vars are fine here
        color=color,       # Vars are fine here
        display="inline-flex",
        align_items="center",
        justify_content="center",
        min_width="76px",
        text_align="center",
    )

def _actions() -> rx.Component:
    return rx.hstack(
        rx.icon(tag="trending-up", size=16),
        rx.icon(tag="users", size=16),
        rx.icon(tag="edit-3", size=16),
        spacing="3",
        justify="end",
        width="100%",
        color="#0F172A",
    )

def _header_row() -> rx.Component:
    return rx.box(
        rx.grid(
            rx.text("Name", weight="medium"),
            rx.text("Role", weight="medium"),
            rx.text("Type", weight="medium"),
            rx.text("Department", weight="medium"),
            rx.text("Actions", weight="medium"),
            columns="5",
            gap="16px",
            width="100%",
            class_name="resources-table-grid",
        ),
        padding_y="12px",
        padding_x="16px",
        border_bottom="1px solid #E5E7EB",
        bg="#FFFFFF",
        position="sticky",
        top="0",
        z_index="1",
        border_top_left_radius="12px",
        border_top_right_radius="12px",
    )

def _row(r) -> rx.Component:
    # r is a Var; use indexing (r["..."]) and pass Vars through unchanged.
    return rx.box(
        rx.grid(
            rx.text(r["name"], weight="medium"),
            rx.text(r["role"]),
            _type_badge(r["type"], r["type_color"], r["type_bg"]),
            rx.text(r["department"]),
            _actions(),
            columns="5",
            gap="16px",
            width="100%",
            class_name="resources-table-grid",
            align="center",
        ),
        padding_y="14px",
        padding_x="16px",
        border_bottom="1px solid #E2E8F0",
        bg="#FFFFFF",
        _hover={"background": "#F8FAFC"},
    )

def table() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("All Resources", weight="bold"),
            padding="16px",
            border_bottom="1px solid #E5E7EB",
            bg="#FFFFFF",
            border_top_left_radius="12px",
            border_top_right_radius="12px",
        ),
        _header_row(),
        rx.foreach(State.filtered_resources, _row),
        bg="#FFFFFF",
        border="1px solid #E5E7EB",
        border_radius="12px",
        overflow="hidden",
        class_name="resources-table",
        width="100%",
    )
