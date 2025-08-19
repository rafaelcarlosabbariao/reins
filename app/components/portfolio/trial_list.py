# app/components/portfolio/trial_list.py
from __future__ import annotations
import reflex as rx
from app.state import AppState as State

# --- reactive-safe badge helpers ---------------------------------------------
def _status_badge(status: rx.Var) -> rx.Component:
    return rx.cond(
        (status == "Ongoing"),
        rx.box(
            rx.text(status, size="1", weight="regular", color="#059669"),
            padding_x="8px",
            padding_y="4px",
            border_radius="9999px",
            style={"background": "#D1FAE5"},
        ),
        rx.cond(
            (status == "Planning"),
            rx.box(
                rx.text(status, size="1", weight="regular", color="#F59E0B"),
                padding_x="8px",
                padding_y="4px",
                border_radius="9999px",
                style={"background": "#FEF3C7"},
            ),
            rx.box(
                rx.text(status, size="1", weight="regular", color="#334155"),
                padding_x="8px",
                padding_y="4px",
                border_radius="9999px",
                style={"background": "#E2E8F0"},
            ),
        ),
    )

def _phase_pill(phase: rx.Var) -> rx.Component:
    return rx.box(
        rx.text(phase, size="1", weight="regular", color="#475569"),
        padding_x="8px",
        padding_y="4px",
        border_radius="9999px",
        style={"background": "#EEF2FF"},
    )

def _protocol_badge(pid: rx.Var) -> rx.Component:
    return rx.box(
        rx.text(pid, size="1", weight="regular", color="#475569"),
        padding_x="8px",
        padding_y="4px",
        border_radius="8px",
        style={"background": "#F1F5F9"},
    )

def _bullet() -> rx.Component:
    return rx.text("•", size="1", color="#CBD5E1")

def _resource_count_pill(count_var: rx.Var) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(tag="users", size=14, color="#64748B"),
            rx.text(count_var, size="1", weight="regular", color="#475569"),
            spacing="1",
            align="center",
        ),
        padding_x="8px",
        padding_y="4px",
        border_radius="9999px",
        style={"background": "#F1F5F9"},
    )

# --- individual trial card ----------------------------------------------------
def trial_card(t: dict) -> rx.Component:
    # selection indicator uses reactive expression with '=='
    selected_bar = rx.cond(
        (State.selected_trial_id == t["protocol_id"]),
        rx.box(position="absolute", left="0", top="0", bottom="0", width="3px", bg="#3B82F6"),
    )

    return rx.box(
        selected_bar,  # child, not a prop
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.link(
                        rx.text(t["title"], weight="bold", color="#0F172A"),
                        href="#",
                        # important: call the action directly (no lambda)
                        on_click=State.select_trial(t["protocol_id"]),
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="eye", size=16, color="#94A3B8"),
                    rx.icon(tag="edit", size=16, color="#94A3B8"),
                    spacing="3",
                    align="center",
                ),
                width="100%",
            ),
            rx.hstack(
                _status_badge(t["status"]),
                _bullet(),
                _protocol_badge(t["protocol_id"]),
                _bullet(),
                _phase_pill(t["phase"]),
                _bullet(),
                _resource_count_pill(t.get("resource_count", 0)),
                spacing="2",
                align="center",
                # wrap="wrap",
            ),
            spacing="2",
            align="start",
        ),
        position="relative",
        padding="16px",
        border_radius="16px",
        box_shadow="0 6px 18px rgba(15,23,42,0.06)",
        bg="white",
    )

# --- scrollable list panel ----------------------------------------------------
def trials_panel() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(tag="flask-conical", size=18, color="#334155"),
                    rx.text("Clinical Trials", weight="bold", color="#000000"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                align="center",
                width="100%",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(State.filtered_trials_with_counts, lambda t: trial_card(t)),
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                type="auto",
                scrollbars="vertical",
                height="65vh",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="16px",
        bg="#F8FAFC",
        border_radius="16px",
        box_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
    )

__all__ = ["trials_panel", "trial_card"]
