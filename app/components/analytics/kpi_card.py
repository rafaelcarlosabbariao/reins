import reflex as rx

def kpi_card(label: str, value: str, description: str = "") -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(label, weight="bold"),
            rx.heading(value, size="7"),
            rx.text(description, size="2"),
            spacing="2",
            align="start",
        ),
        width="100%",
        padding="1rem",
        radius="lg",
        shadow="sm",
    )