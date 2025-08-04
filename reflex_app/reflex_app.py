# reflex_app/app.py

import reflex as rx

# 1. Import State classes
from reflex_app.state.resource_state import ResourceState
from reflex_app.state.study_state import StudyState
from reflex_app.state.demand_state import DemandState

# 2. Import Pages and Global Layout
from reflex_app.pages.home import HomePage
from reflex_app.pages.portfolio_dashboard import PortfolioDashboardPage
# from reflex_app.pages.capacity_planner import CapacityPlannerPage
# from reflex_app.pages.demand_backlog import DemandBacklogPage
# from reflex_app.pages.scenarios import ScenariosPage
from reflex_app.components.app_shell import AppShell

# 3. Initialize the Reflex app with your State modules
app = rx.App(_state=[ResourceState, StudyState, DemandState],
             layout=AppShell)

# # 4. Apply the global layout (Navbar, Footer, theme)
# app.set_layout(AppShell)

# 5. Register pages with paths and titles
app.add_page(HomePage, title="REINS Home", path="/")
app.add_page(PortfolioDashboardPage, title="Portfolio Dashboard", path="/portfolio")
# app.add_page(CapacityPlannerPage, title="Capacity Planner", path="/capacity")
# app.add_page(DemandBacklogPage, title="Demand Backlog", path="/demand")
# app.add_page(ScenariosPage, title="Scenario Modeling", path="/scenarios")

# 6. Compile for deployment or local dev
if __name__ == "__main__":
    app.compile()
