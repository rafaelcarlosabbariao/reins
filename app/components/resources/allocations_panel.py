import reflex as rx
from app.state import AppState as State

def _kpi_card(value: str, label: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(value, weight="bold", size="6"),
            rx.text(label, color="#64748B"),
            spacing="1",
            align="start",
        ),
        bg="#FFFFFF",
        border="1px solid #E5E7EB",
        border_radius="12px",
        padding="16px",
        width="100%",
    )

def _alloc_header() -> rx.Component:
    # Title row with back button and "Add Allocation"
    return rx.hstack(
        rx.hstack(
            rx.button(
                rx.icon(tag="arrow-left"),
                variant="soft",
                radius="full",
                on_click=State.close_allocations,
            ),
            rx.vstack(
                rx.heading(rx.text(State.selected_resource["name"]), size="6"),
                rx.text(
                    rx.fragment(
                        State.selected_resource["role"],
                        " • ",
                        State.selected_resource["department"],
                    ),
                    color="#64748B",
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        rx.spacer(),
        rx.button(
            rx.hstack(rx.icon(tag="plus", size=16), rx.text("Add Allocation")),
            variant="solid",
            radius="large",
        ),
        align="center",
        width="100%",
    )

def _alloc_table_header() -> rx.Component:
    return rx.grid(
        rx.text("Trial", weight="medium"),
        rx.text("Phase", weight="medium"),
        rx.text("Allocation", weight="medium"),
        rx.text("Weekly Hours", weight="medium"),
        rx.text("Duration", weight="medium"),
        rx.text("Actions", weight="medium"),
        columns="6",
        gap="16px",
        padding_y="10px",
        padding_x="16px",
        bg="#FFFFFF",
        border_bottom="1px solid #E5E7EB",
        class_name="alloc-table-grid",
        width="100%",
    )

def _alloc_row(a) -> rx.Component:
    return rx.box(
        rx.grid(
            rx.text(a["trial"], weight="medium"),
            rx.text(a["phase"]),
            rx.text(a["allocation"]),
            rx.text(a["weekly_hours"]),
            rx.hstack(
                rx.icon(tag="calendar", size=14),
                rx.text(
                    rx.fragment(a["start_date"], " to ", a["end_date"])
                ),
                spacing="2",
                align="center",
            ),
            rx.hstack(rx.icon(tag="edit-3", size=16)),
            columns="6",
            gap="16px",
            class_name="alloc-table-grid",
            width="100%",
            align="center",
        ),
        padding_y="12px",
        padding_x="16px",
        bg="#FFFFFF",
        border_bottom="1px solid #E5E7EB",
    )

def _alloc_table() -> rx.Component:
    return rx.box(
        _alloc_table_header(),
        rx.cond(
            State.has_selected_allocations,
            rx.foreach(State.selected_resource_allocations, _alloc_row),
            rx.box(
                rx.text("No allocations found."),
                padding="16px",
                bg="#FFFFFF",
            ),
        ),
        border="1px solid #E5E7EB",
        border_radius="12px",
        overflow="hidden",
        bg="#FFFFFF",
    )

def allocations_panel() -> rx.Component:
    # Full-screen overlay; simple and robust (no 3rd-party event triggers)
    return rx.cond(
        State.allocations_open,
        rx.box(
            # Scrim
            rx.box(
                position="fixed",
                inset="0",
                bg="rgba(15, 23, 42, 0.45)",
                z_index="50",
            ),
            # Panel
            rx.box(
                rx.vstack(
                    _alloc_header(),
                    # KPI row (optional placeholders; remove if you prefer)
                    rx.grid(
                        _kpi_card("40h", "Weekly Capacity"),
                        _kpi_card("60%", "Total Allocation"),
                        _kpi_card("24h", "Weekly Hours"),
                        _kpi_card("2", "Active Trials"),
                        columns="4",
                        gap="16px",
                        width="100%",
                    ),
                    _alloc_table(),
                    spacing="4",
                    width="100%",
                ),
                class_name="allocations-panel",
                position="fixed",
                inset="4% 6%",
                bg="#F8FAFC",
                border_radius="16px",
                padding="20px",
                z_index="51",
                overflow="auto",
            ),
        ),
        rx.fragment(),
    )