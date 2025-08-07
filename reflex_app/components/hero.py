# reflex_app/components/hero.py

import reflex as rx

def Hero():
    # Top‐level container with background image
    return rx.box(
        background_image="url('/assets/lab-banner.jpg')",
        background_size="cover",
        background_position="center",
        pos="relative",
        w="100%",
        h="60vh",
    )(
        # Overlay tint
        rx.box(
            bg="rgba(0,53,128,0.6)",
            pos="absolute",
            top="0",
            left="0",
            w="100%",
            h="100%",
            z_index=0,
        ),
        # Centered content
        rx.vstack(
            rx.heading(
                "REINS: Your CD&O Resource Command Center",
                size="4xl",
                color="white",
            ),
            rx.text(
                "Portfolio-centric insights. Real-time resource wellness.",
                size="lg",
                color="white",
            ),
            rx.hstack(
                rx.button(
                    "Explore Portfolios",
                    on_click=lambda: None,
                    size="lg",
                ),
                rx.button(
                    "Quick Filters",
                    variant="outline",
                    on_click=lambda: None,
                    size="lg",
                ),
                spacing="1rem",
            ),
            align="center",
            justify="center",
            h="100%",
            pos="relative",
            z_index=1,
        ),
    )
