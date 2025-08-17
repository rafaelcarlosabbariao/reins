import reflex as rx

def logo() -> rx.Component:
    return rx.hstack(
        rx.image(
            src="/logo/reins_logo.png",
            width="36px",
            height="54px",
            radius="md"
        ),
        rx.vstack(
            rx.text("REINS", weight="bold", color="black"),
            rx.text("Resourcing Insights & Standards", size="1", color="gray"),
            spacing="0",
            align="start",
        ),
        spacing="3",
        align="center",
        width="100%"
    )
