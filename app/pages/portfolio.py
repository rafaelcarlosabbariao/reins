# app/pages/portfolio.py
from __future__ import annotations
import reflex as rx
from app.state import AppState as State
from app.components.portfolio.kpi_card import kpi_card
from app.components.portfolio.trial_list import trials_panel
from app.components.portfolio.filter_bar import filter_bar
from app.components.portfolio.resource_summary import resource_summary_strip
from app.components.portfolio.resource_type_pie import resource_type_pie
from app.components.portfolio.functional_area_pie import functional_area_pie
from app.components.portfolio.resources_by_department import resources_by_department_chart
from app.components.portfolio.resource_allocations_table import resource_allocations_table

content_height = "100vh - 220px"

def portfolio_header() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.heading("Portfolio Overview", size="8"),
            rx.text(
                "Clinical trial portfolio and resource allocation management",
                color="#64748B",
            ),
            align="start",
            spacing="2",
        ),
        rx.spacer(),
        rx.button(
            rx.icon(tag="plus", size=16),
            rx.text("Add New Trial", weight="medium"),
            padding_x="14px",
            padding_y="10px",
            border_radius="12px",
            bg="#2563EB",
            color="white",
            _hover={"background": "#1D4ED8"},
        ),
        align="center",
        width="100%",
    )

# Search + Trials list
def trials_search_box() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(tag="search", size=16, color="#0F172A"),
            rx.input(
                value=State.query,
                placeholder="Search trials...", 
                on_change=State.set_query,
                width="100%",
                style={
                    "background":"#FFFFFF",
                    "border":"1px solid #E2E8F0",
                    "boxShadow":"none",
                    "color":"#0F172A",
                }
            ),
            width="100%",
        ),
        padding_x="12px",
        padding_y="10px",
        border_radius="10px",
        box_shadow="inset 0 0 0 1px rgba(255, 255, 255, 0.85), 0 2px 6px rgba(255, 255, 255, 0.85)",
        bg="white",
        width="100%",
    )

def trials_filter() -> rx.Component:
    return rx.vstack(
        trials_search_box(),
        trials_panel(),
        spacing="3",
        align="start",
        width="100%",
        height="100%",
    )

def kpi_strip() -> rx.Component:
    return rx.grid(
        # KPI cards
        kpi_card(
            "Active Trials",
            State.active_trials,            # scalar @rx.var
            icon_text="🧪",
            accent="indigo-sky",
            trend_text=State.planning_text, # scalar @rx.var (string)
            trend_positive=True,
        ),
        kpi_card(
            "Total Resources",
            State.total_resources,          # scalar @rx.var
            subtitle=State.total_resources_sub,
            icon_text="👥",
            accent="emerald",
        ),
        kpi_card(
            "Avg Utilization",
            State.avg_util_value,           # scalar @rx.var (string)
            subtitle=State.avg_util_sub,
            icon_text="📈",
            accent="violet",
        ),
        # columns must be a token or breakpoints mapping (NOT a list of ints)
        columns=rx.breakpoints({"base": "1", "md": "2", "lg": "3"}),
        spacing="4",
        width="100%",
    )

def trial_placeholder() -> rx.Component:
    """Empty state card prompting selection (shown when nothing selected)."""
    icon = rx.icon(tag="flask-conical", size=56, color="#94A3B8", aria_hidden="true")
    return rx.card(
        rx.vstack(
            rx.center(icon),
            rx.center(rx.text("Select a Clinical Trial", weight="bold", size="5", color="#334155")),
            rx.center(
                rx.text(
                    "Choose a trial from the list to view sites, resource analytics and allocation information.",
                    color="#64748B",
                    align="center",
                )
            ),
            spacing="3",
            width="100%",
        ),
        padding="28px",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15,23,42,0.08)",
        width="100%",
    )

def main_content() -> rx.Component:
    return rx.vstack(
        kpi_strip(),
        # show placeholder when nothing selected
        rx.cond(
            (State.selected_trial_id == None),
            trial_placeholder(),
            rx.vstack(
                resource_summary_strip(),
                rx.cond(
                    State.show_resources_table,
                    resource_allocations_table(),
                    rx.vstack(
                        rx.grid(
                            resource_type_pie(),
                            functional_area_pie(),
                            columns=rx.breakpoints({"base":"1", "md":"2"}),
                            spacing="4",
                            width="100%"
                        ),
                        resources_by_department_chart(),
                        spacing="4",
                        width="100%",
                    )
                ),
                spacing="4",
                width="100%",
            ),
        ),
        spacing="4",
        align="start",
        height="100%",
        width="100%",
    )

def two_col_row() -> rx.Component: 
    return rx.flex(
        # Search + Filter list
        rx.box(
            trials_filter(),
            width=rx.breakpoints({"base":"100%", "lg":"34%"}),
        ),
        # KPI Cards + Placeholder/Main Content
        rx.box(
            main_content(),
            width=rx.breakpoints({"base":"100%", "lg":"66%"}),
        ),
        align="start",
        spacing="2",
        width="100%",
    )

def page() -> rx.Component:
    return rx.container(
        rx.vstack(
            portfolio_header(),
            filter_bar(),
            two_col_row(),
            spacing="5",
            align="start",
        ),
        on_mount=State.on_load,
        size="4",
        width="100%",
        max_width="1600px",
        margin_x="auto",
    )

__all__ = ["page"]
