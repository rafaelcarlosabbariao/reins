import reflex as rx

class ReinsConfig(rx.Config):
    app_name: str = "app"
    frontend_packages: list[str] = []

config = ReinsConfig(app_name = "app")