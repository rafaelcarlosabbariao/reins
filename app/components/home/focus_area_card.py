import reflex as rx
from typing import Union

Value = Union[int, str, rx.Var]

def focus_area_card(title: str, count: Value, img: str, href: str) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.image(src=img, alt=title, width="100%", height="180px", object_fit="cover", radius="md"),
                rx.hstack(
                    rx.text(title, weight="bold", color="black"),
                    rx.spacer(),
                    rx.badge(count, size="2"),
                    align="center",
                    width="100%",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            padding="0.75rem",
            radius="xl",
            shadow="sm",
            width="100%",
            height="100%",
            _hover={"boxShadow": "0 10px 28px rgba(0,0,0,0.12)", "transform": "translateY(-2px)"},
            transition="all 0.15s ease",
            background="white"
        ),
        href=href,
        underline="none",
    )
