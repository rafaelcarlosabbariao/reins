# reflex_app/components/hero.py

import reflex as rx

def Hero():
    return rx.box(
        # full-width background image with overlay
        rx.style(
            background_image="url('/assets/lab-banner.jpg')",
            background_size="cover",
            background_position="center",
            position="relative",
            width="100%",
            height="60vh",
        ),
        rx.box(
            # overlay tint
            rx.style(
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                bg="rgba(0,53,128,0.6)",
                z_index="0",
            )
        ),
        rx.vstack(
            rx.heading("REINS: Your CD&O Resource Command Center", size="4xl", color="white"),
            rx.text("Portfolio-centric insights. Real-time resource wellness.", size="lg", color="white"),
            rx.hstack(
                rx.button("Explore Portfolios", on_click=lambda: None, size="lg"),
                rx.button("Quick Filters", variant="outline", on_click=lambda: None, size="lg"),
                spacing="1rem",
            ),
            align="center",
            justify="center",
            height="100%",
            position="relative",
            z_index="1",
        ),
    )
