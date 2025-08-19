import reflex as rx
from typing import Union

Value = Union[int, float, str, rx.Var]

card_shape = dict(
    padding="1rem",
    radius="2xl",                            # rounder corners
    width="100%",
    background="linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.98))",
    border="1px solid rgba(2,6,23,.06)",     # ultra-thin border
    box_shadow="0 6px 16px rgba(2,6,23,.06)",# soft shadow
    transition="all .18s ease",
    _hover={
        "boxShadow": "0 12px 28px rgba(2,6,23,.10)",
        "transform": "translateY(-2px)",
        "cursor": "pointer",
    },
)

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
            **card_shape,
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
            radius="2xl",
            width="100%",
            shadow="lg",
            background="linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)",
            position="relative",
            overflow="hidden",
            box_shadow="0 14px 36px rgba(37, 99, 235, 0.28)",
            _hover={
                "boxShadow": "0 18px 44px rgba(37, 99, 235, 0.35)",
                "transform": "translateY(-2px)",
                "cursor": "pointer",
            },
            _after={
                "content": "''",
                "position": "absolute",
                "right": "-20px",
                "top": "-20px",
                "width": "180px",
                "height": "180px",
                "background": "radial-gradient(closest-side, rgba(255,255,255,.35), rgba(255,255,255,0) 70%)",
                "filter": "blur(2px)",
            },
            transition="all 0.18s ease",
        ),
        href=href,
        underline="none",
    )
