import reflex as rx

def hero() -> rx.Component:
    return rx.vstack(
        rx.text("ABOUT", size="1", color="blue", letter_spacing="0.08em"),
        rx.heading(
            "Starting with our commitment to excellence, our people have always been innovators and trailblazers, committed to finding the next breakthrough.",
            size="8",
            color="black"
        ),
        rx.text(
            "This application provides a portfolio-centric view to manage and allocate resources efficiently across all phases of clinical trials, maintaining our standard 60:40 FTE to FSP/Contractor ratio.",
            size="3",
            color="black"
        ),
        rx.hstack(
            rx.button("Learn More About Our Portfolio", on_click=rx.redirect("/portfolio")),
            # rx.button(
            #     "Explore the Product Pipeline",
            #     variant="soft",
            #     on_click=rx.redirect("/portfolio?view=pipeline"),
            # ),
            spacing="3",
            wrap="wrap",
        ),
        spacing="3",
        width="60%",
        align="start",
    )
