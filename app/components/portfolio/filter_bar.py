from __future__ import annotations
import reflex as rx
from app.state import AppState as State

def _chip_select(
        value: rx.Var,
        items: rx.Var | list[str],
        on_change,
        placeholder: str,
) -> rx.Component:
    """
    a chip-styled select (rounded, subtle shadow)
    """
    return rx.box(
        rx.select(
            items=items,
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            # keep using the simple select; style the visible control here
            size="2",
            radius="full",
            width="100%",
            # these props land on the trigger in the simple API
            color="#0F172A",           # text color
            bg="#FFFFFF",              # background
            border="1px solid #E2E8F0",
            box_shadow="0 1px 2px rgba(15,23,42,0.05)",
            padding="6px 10px",
            # make placeholder and states consistent
            _placeholder={"color": "#0F172A"},
            _hover={"bg": "#FFFFFF"},
            _active={"bg": "#FFFFFF"},
            _focus={"bg": "#FFFFFF", "outline": "none", "boxShadow": "0 0 0 1px #93C5FD"},
        ),
        width="100%",
    )

def filter_bar() -> rx.Component:
    """Filter bar shown under the page header and above KPI cards."""
    icon_chip = rx.box(
        rx.icon(tag="filter", size=16, color="#64748B"),
        padding_x="12px",
        padding_y="10px",
        border_radius="10px",
        box_shadow="inset 0 1px 2px rgba(15,23,42,0.05)",
        bg="white",
    )

    chips_grid = rx.grid(
        _chip_select(State.status, State.status_options, State.set_status, "All Status"),
        _chip_select(State.phase, State.phase_options, State.set_phase, "All Phases"),
        _chip_select(State.priority, State.priority_options, State.set_priority, "All Priority"),
        _chip_select(State.therapeutic_area, State.area_options, State.set_therapeutic_area, "All Areas"),
        _chip_select(State.department, State.department_options, State.set_department, "All Departments"),
        columns=rx.breakpoints({"base": "1", "sm": "2", "md": "3", "lg": "5"}),
        spacing="3",
        width="100%",
    )

    return rx.box(
        rx.flex(
            icon_chip,
            rx.box(
                chips_grid,
                flex_grow="1",
                width="100%",
                min_width="240px",
            ),
            align="center",
            width="100%",
            column_gap="3",
            row_gap="3"
    ),
    bg="#F8FBFF",
    padding="10px",
    border_radius="12px",
    box_shadow="0 6px 18px rgba(15,23,42,0.06)",
    width="100%",
    )