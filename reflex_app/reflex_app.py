# reflex_app/app.py

import reflex as rx

# Import State classes
from reflex_app.state.resource_state import ResourceState
from reflex_app.state.study_state import StudyState
from reflex_app.state.demand_state import DemandState

# Import Pages and Global Layout
from reflex_app.pages.home import HomePage
from reflex_app.pages.portfolio_dashboard import PortfolioDashboardPage
# from reflex_app.pages.capacity_planner import CapacityPlannerPage
# from reflex_app.pages.demand_backlog import DemandBacklogPage
# from reflex_app.pages.scenarios import ScenariosPage
from reflex_app.components.app_shell import AppShell

# Initialize the Reflex app with your State modules
app = rx.App(
    theme = rx.theme(accent_color="blue"),
    style = {"fontFamily": "Inter, sans-serif"},
    reset_style = True,
    head_components = [
        rx.el.link(rel="icon", href="C:/Users/Raf/Documents/Projects/reins/assets/logo-blue.png"),
        rx.el.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
    ],
    app_wraps = {
        (10, "AppShell"): lambda stateful: AppShell()
    }
)

# # Register State classes
# app.add_state(ResourceState)
# app.add_state(StudyState)
# app.add_state(DemandState)

# Register pages with paths and titles
app.add_page(HomePage, title="REINS Home")
app.add_page(PortfolioDashboardPage, title="Portfolio Dashboard")
# app.add_page(CapacityPlannerPage, title="Capacity Planner", path="/capacity")
# app.add_page(DemandBacklogPage, title="Demand Backlog", path="/demand")
# app.add_page(ScenariosPage, title="Scenario Modeling", path="/scenarios")

# Compile for deployment or local dev
if __name__ == "__main__":
    app.compile()
