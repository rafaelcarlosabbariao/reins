import reflex as rx
from app.state import AppState as State
from app.components.portfolio.metric_card import metric_card
from app.components.portfolio.filter_bar import filter_bar
from app.components.portfolio.trial_list import trial_list
from app.components.portfolio.resource_analytics_strip import analytics_strip
from app.components.portfolio.charts import resource_type_donut, functional_area_donut, hours_by_dept_bar
from app.components.portfolio.resource_list import resource_list
from app.components.portfolio.sites_map import sites_map

def empty_selection() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Select a Clinical Trial", size="6"),
            rx.text("Choose a trial from the list to view sites, resource analytics and allocation information.", size="2", color="gray"),
            spacing="2", align="center", width="100%",
        ),
        padding="2rem", radius="xl", shadow="sm", width="100%", height="16rem",
        display="grid", place_items="center",
    )

def selected_view() -> rx.Component:
    #    ┌─ strip
    #    ├─ small grid: two donuts
    #    ├─ bar chart
    #    ├─ resource list
    #    └─ sites map
    return rx.vstack(
        analytics_strip(),
        rx.grid(
            rx.card(resource_type_donut(), padding="0.5rem", radius="xl", shadow="sm", width="100%"),
            rx.card(functional_area_donut(), padding="0.5rem", radius="xl", shadow="sm", width="100%"),
            columns="2", gap="4", width="100%",
        ),
        rx.card(hours_by_dept_bar(), padding="0.5rem", radius="xl", shadow="sm", width="100%"),
        resource_list(),
        sites_map(),
        spacing="4", width="100%", align="start",
    )

def right_panel() -> rx.Component:
    return rx.cond(State.has_selection, empty_selection(), selected_view())

def view() -> rx.Component:
    header = rx.vstack(
        rx.hstack(
            rx.heading("Portfolio Overview", size="8"),
            rx.spacer(),
            rx.button("+  Add New Trial", class_name="reins-btn reins-btn--primary"),
            align="center", width="100%",
        ),
        rx.text("Clinical trial portfolio and resource allocation management", size="2", color="gray"),
        spacing="2", width="100%", align="start",
    )

    kpis = rx.grid(
        metric_card("Active Trials", State.portfolio_active_trials, f"{State.portfolio_in_planning} in planning", "/icons/lab.svg"),
        metric_card("Total Resources", State.portfolio_total_resources, f"{State.portfolio_fte_share}% FTE, {State.portfolio_fsp_share}% FSP", "/icons/resources.svg"),
        metric_card("Avg Utilization", f"{State.portfolio_avg_util}%", "Balanced workload", "/icons/analytics.svg"),
        columns="3", gap="4", width="100%",
    )

    filters = rx.card(filter_bar(), padding="0.75rem", radius="xl", shadow="sm", width="100%")

    content = rx.grid(
        rx.box(trial_list(), width="100%"),
        rx.box(right_panel(), width="100%"),
        columns="2", gap="4", width="100%", align="start",
    )

    return rx.vstack(header, kpis, filters, content, spacing="4", width="100%", align="start")
