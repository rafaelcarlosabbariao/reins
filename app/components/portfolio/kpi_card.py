from __future__ import annotations
import reflex as rx

def kpi_card(
    title: str,
    value: str | int | float | rx.Var,
    subtitle: str | None = None,
    *,
    icon_text: str = "•",
    accent: str = "indigo-sky",          # indigo-sky | emerald | violet
    trend_text: str | None = None,
    trend_positive: bool = True,
) -> rx.Component:
    grads = {
        "indigo-sky": {
            "bubble": "linear-gradient(135deg, #E0E7FF 0%, #CFFAFE 100%)",
            "pill":   "linear-gradient(135deg, #4F46E5 0%, #0EA5E9 100%)",
        },
        "emerald": {
            "bubble": "linear-gradient(135deg, #DCFCE7 0%, #D1FAE5 100%)",
            "pill":   "linear-gradient(135deg, #10B981 0%, #34D399 100%)",
        },
        "violet": {
            "bubble": "linear-gradient(135deg, #EDE9FE 0%, #F5D0FE 100%)",
            "pill":   "linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%)",
        },
    }
    g = grads.get(accent, grads["indigo-sky"])
    trend_color = "#059669" if trend_positive else "#DC2626"
    trend_icon = "trending-up" if trend_positive else "trending-down"

    # Build the main text stack
    text_stack = rx.vstack(
        rx.text(
            title,
            size="2",
            color="#64748B",
            weight="medium",
            transform="uppercase",
            letter_spacing="0.08em",
        ),
        rx.text(value, size="8", weight="bold", color="#0F172A", line_height="1.1"),
        rx.cond(subtitle is not None, rx.text(subtitle, size="2", color="#475569")),
        align="start",
        spacing="2",
    )

    # Right-side icon pill
    icon_pill = rx.box(
        rx.text(icon_text, size="6"),
        width="56px",
        height="56px",
        min_width="56px",
        border_radius="16px",
        display="flex",
        align_items="center",
        justify_content="center",
        color="white",
        font_weight="700",
        style={"background": g["pill"], "boxShadow": "0 6px 16px rgba(0,0,0,0.12)"},
        aria_hidden="true",
    )

    # Optional trend row
    trend_row = rx.cond(
        trend_text is not None,
        rx.hstack(
            rx.icon(tag=trend_icon, size=16, color=trend_color),
            rx.text(trend_text, size="2", weight="medium", color=trend_color),
            margin_top="10px",
            align="center",
            spacing="2",
        ),
    )

    return rx.box(
        # faint gradient bubble background
        rx.box(
            position="absolute",
            top="-28px",
            right="-28px",
            width="160px",
            height="160px",
            border_radius="9999px",
            style={"background": g["bubble"], "opacity": 0.55},
        ),
        # content row
        rx.hstack(
            text_stack,
            icon_pill,
            align="start",
            justify="between",
            width="100%",
        ),
        # optional trend
        trend_row,
        position="relative",
        bg="white",
        border_radius="16px",
        box_shadow="0 10px 30px rgba(15, 23, 42, 0.08)",
        padding="20px",
        min_height="120px",
        overflow="hidden",
        transition="transform 120ms ease, box-shadow 120ms ease",
        _hover={"transform": "translateY(-2px)", "boxShadow": "0 14px 36px rgba(15, 23, 42, 0.12)"},
    )
