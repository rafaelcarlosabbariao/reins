import reflex as rx
from app.state import AppState as State

def sites_map() -> rx.Component:
    # Only render when a trial is selected (prevents Var truthiness issues)
    return rx.cond(
        State.has_selection,
        rx.card(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.text(
                        rx.fragment("Study Sites: ", State.selected_trial["title"]),
                        size="3",
                        weight="bold",
                    ),
                    rx.spacer(),
                    rx.badge(State.selected_trial["id"], size="2"),
                    rx.badge(
                        State.selected_trial["phase"],
                        size="2",
                        background="#E8F5E9",
                        color="#147D2B",
                    ),
                    rx.badge(State.sel_sites_counts_label, size="2"),
                    align="center",
                    width="100%",
                    wrap="wrap",
                    gap="2",
                ),
                # Body (map placeholder)
                rx.box(
                    rx.text("Map placeholder (Leaflet/Mapbox here)", color="gray"),
                    height="22rem",
                    width="100%",
                    background="#F8FAFC",
                    border="1px solid #E5E7EB",
                    radius="lg",
                    display="grid",
                    place_items="center",
                ),
                spacing="3",
                width="100%",
                align="start",
            ),
            padding="0.75rem",
            radius="xl",
            shadow="sm",
            width="100%",
        ),
        rx.box(),  # nothing when no selection
    )
