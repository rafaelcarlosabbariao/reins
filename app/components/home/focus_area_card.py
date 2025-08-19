import reflex as rx
from typing import Union

Value = Union[int, str, rx.Var]

badge = dict(
    background="#2563EB",
    color="white",
    font_weight="bold",
    font_size="1rem",
    text_align="center",
    height="2rem",
    box_shadow="0 10px 24px rgba(37,99,235,.28)",   # soft lift like Base44
)

card = dict(
    padding="0.75rem",
    radius="2xl",
    background="linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.98))",
    border="1px solid rgba(2,6,23,.06)",
    box_shadow="0 6px 16px rgba(2,6,23,.06)",
    transition="all .18s ease",
    _hover={"boxShadow": "0 12px 28px rgba(2,6,23,.10)", "transform": "translateY(-2px)"},
)

def focus_area_card(title: str, count: Value, img: str, href: str) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                # Image with subtle bottom fade (like the mock)
                rx.box(
                    rx.image(
                        src=img,
                        alt=title,
                        width="100%",
                        height="clamp(160px, 20vw, 220px)",
                        object_fit="cover",
                        object_position="center",
                        display="block",
                    ),
                    # gradient overlay on the lower part of the image
                    rx.box(
                        position="absolute",
                        left="0",
                        right="0",
                        bottom="0",
                        height="42%",
                        background="linear-gradient(180deg, rgba(2,6,23,0) 0%, rgba(2,6,23,.42) 100%)",
                    ),
                    position="relative",
                    width="100%",
                    overflow="hidden",
                    radius="xl",
                ),

                # Footer row: title left, count pill right
                rx.hstack(
                    rx.text(title, weight="bold", color="black"),
                    rx.badge(count, **badge),
                    justify="between",
                    align="start",
                    width="100%",
                    padding_top=".65rem",
                ),
                spacing="2",
                width="100%",
            ),
            width="100%",
            height="100%",
            **card,
        ),
        href=href,
        underline="none",
    )
