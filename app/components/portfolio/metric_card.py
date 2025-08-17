import reflex as rx

def metric_card(title: str, value: str | int, subtitle: str = "", icon: str | None = None) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(title.upper(), size="1", color="gray", letter_spacing="0.08em"),
                rx.heading(str(value), size="8"),
                rx.text(subtitle, size="2", color="gray"),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.cond(
                icon is not None,
                rx.box(
                    rx.image(src=icon, alt="", width="28px", height="28px"),
                    width="48px", height="48px",
                    background="#EEF2FF", radius="full",
                    display="grid", place_items="center",
                ),
                rx.box(),  # empty
            ),
            align="center",
            width="100%",
        ),
        padding="1rem",
        radius="xl",
        shadow="sm",
        width="100%",
        class_name="reins-card",
    )
