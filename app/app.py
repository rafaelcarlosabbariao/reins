import reflex as rx 
from app.components.sidebar.logo import logo
from app.components.sidebar.nav import navigation
from app.components.sidebar.ratio_card import ratio_card
from app.components.sidebar.user_card import user_card

def sidebar(current: str) -> rx.Component:
    return rx.vstack(
        logo(),
        rx.box(height="1rem"),
        navigation(current=current),
        rx.box(height="1rem"),
        ratio_card(),
        rx.spacer(),
        user_card(),
        align="start",
        width="16rem",
        padding="1rem",
        border_right="1px solid #E5E7EB",
        height="100vh",
        position="sticky",
        top="0",
        background="#F3F4F6"
    )

def layout(current: str, *children) -> rx.Component:
    return rx.hstack(
        sidebar(current),
        rx.box(
            *children,
            width="100%",
            padding="1.25rem",
            background="white",
        ),
        align="start",
        width="100%",
        background="#F6F8FB"
    )

@rx.page(route="/", title="Home")
def index() -> rx.Component:
    from app.pages.home import page
    return layout("/", page())

@rx.page(route="/portfolio", title="Portfolio")
def portfolio() -> rx.Component:
    from app.pages.portfolio import page
    return layout("/portfolio", page())

@rx.page(route="/resources", title="Resources")
def resources() -> rx.Component:
    from app.pages.resources import page
    return layout("/resources", page())

@rx.page(route="/timeline", title="Timeline")
def timeline() -> rx.Component:
    from app.pages.timeline import view
    return layout("/timeline", view())

@rx.page(route="/analytics", title="Analytics")
def analytics() -> rx.Component:
    from app.pages.analytics import view
    return layout("/analytics", view())


app = rx.App(
    stylesheets=["/index.css"]
)