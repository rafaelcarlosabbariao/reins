import reflex as rx
from app.state import AppState as State
from app.components.home.pipeline_counts_card import pipeline_counts_card, pipeline_total_card
from app.components.home.focus_area_card import focus_area_card
from app.components.home.hero import hero

def view() -> rx.Component:
    return rx.vstack(
        # ABOUT / HERO
        hero(),
        rx.box(height="1rem"),

        # Pipeline header + snapshot date
        rx.hstack(
            rx.text("Pipeline Snapshot as of", size="2", color="gray", weight="light"),
            rx.text(State.pipeline_snapshot_asof, size="2", color="gray", weight="light"),
            align="center",
            white_space="nowrap"
        ),

        # Phase tiles + Total highlight
        rx.grid(
            rx.foreach(
                State.phase_counts,
                lambda it: pipeline_counts_card(it["label"], it["value"], f"/portfolio?phase={it['phase']}")
            ),
            pipeline_total_card(State.phase_total, "/portfolio"),
            columns="5",
            gap="1rem",
            width="100%",
        ),

        # Primary/secondary actions under tiles
        rx.hstack(
            rx.button("Explore the Product Pipeline", on_click=rx.redirect("/portfolio?view=pipeline")),
            # rx.button("Download Complete Pipeline PDF", variant="soft", on_click=lambda: None),
            spacing="3",
            wrap="wrap",
        ),
        rx.box(height="1.25rem"),

        # AREAS OF FOCUS
        rx.text("AREAS OF FOCUS", size="1", color="blue", letter_spacing="0.08em"),
        rx.heading(
            "Revolutionary medicines enable us to enrich and extend life for people living with all types of diseases.",
            size="7",
            width="60%",
        ),
        rx.grid(
            rx.foreach(
                State.therapeutic_areas,
                lambda it: focus_area_card(it["title"], it["count"], it["img"], it["href"]),
            ),
            columns="4",
            gap="1rem",
            width="100%",
        ),

        spacing="4",
        width="100%",
        align="start",
        background="white"
    )