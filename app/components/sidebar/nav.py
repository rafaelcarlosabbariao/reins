import reflex as rx

def _nav_item(label: str, href: str, icon_src: str, active: bool = False) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.image(
                src=icon_src,
                alt=f"{label} icon",
                width="18px",
                height="18px",
                display="block",
                opacity="1.0" if active else "0.8",
            ),
            rx.text(
                label,
                size="2",
                weight="medium" if active else "regular",
                color="#111827" if active else "#374151",
            ),
            rx.spacer(),
            rx.box(
                width="6px",
                height="6px",
                radius="full",
                background="#2563EB" if active else "transparent",
            ),
            align="center",
            width="100%",
            gap="8px",
        ),
        href=href,
        underline="none",
        padding_y="0.5rem",
        padding_x="0.5rem",
        radius="md",
        background="#F3F4F6" if active else "transparent",
        _hover={"background": "#F8FAFC"},
        aria_current="page" if active else "false",
    )

def navigation(current: str = "/") -> rx.Component:
    base_items = [
        {"label": "Home",      "href": "/",          "icon": "/icons/home.svg"},
        {"label": "Portfolio", "href": "/portfolio", "icon": "/icons/portfolio.svg"},
        {"label": "Resources", "href": "/resources", "icon": "/icons/resources.svg"},
        {"label": "Timeline",  "href": "/timeline",  "icon": "/icons/timeline.svg"},
        {"label": "Analytics", "href": "/analytics", "icon": "/icons/analytics.svg"},
    ]

    def is_active(path: str) -> bool:
        return (current == path) if path == "/" else current.startswith(path)

    items = [{**it, "active": is_active(it["href"])} for it in base_items]

    # build with plain Python so `active` is a real bool (not a Var)
    rows = [
        _nav_item(it["label"], it["href"], it["icon"], it["active"])
        for it in items
    ]

    return rx.vstack(
        rx.text("NAVIGATION", size="1", color="gray", letter_spacing="0.08em"),
        *rows,
        spacing="1",
        align="start",
        width="100%",
    )
