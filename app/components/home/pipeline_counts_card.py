import reflex as rx
from typing import Union

Value = Union[int, float, str, rx.Var]

def pipeline_counts_card(label: str, value: Value, href: str = "#") -> rx.Component:
    return rx.link(
        rx.card(
            rx.center(
                rx.vstack(
                    rx.heading(value, size="8"),
                    rx.text(label, size="2", color="blue"),
                    spacing="1",
                    align="center",
                ),
                min_height="7rem",
            ),
            padding="1rem",
            radius="xl",
            shadow="sm",
            width="100%",
            border="1px solid #E5E7EB",
            background="white",
            _hover={
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "transform": "translateY(-2px)",
                "cursor": "pointer",
            },
            transition="all 0.15s ease",
        ),
        href=href,
        underline="none",
    )

def pipeline_total_card(value: Value, href: str = "#") -> rx.Component:
    return rx.link(
        rx.card(
            rx.center(
                rx.vstack(
                    rx.heading(value, size="8", color="white"),
                    rx.text("Total", size="2", color="rgba(255,255,255,0.9)"),
                    spacing="1",
                    align="center",
                ),
                min_height="7rem",
            ),
            padding="1rem",
            radius="xl",
            width="100%",
            shadow="lg",
            background="linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)",
            _hover={
                "boxShadow": "0 4px 16px rgba(0,0,0,0.15)",
                "transform": "translateY(-2px)",
                "cursor": "pointer",
            },
            transition="all 0.15s ease",
        ),
        href=href,
        underline="none",
    )
