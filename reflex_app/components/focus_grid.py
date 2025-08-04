# reflex_app/components/focus_grid.py

import reflex as rx

functions = [
    ("Oncology", "FaFlask"),
    ("Vaccines", "FaSyringe"),
    ("IM/I&I", "FaHeartbeat"),
    ("Site Ops", "FaMapMarkerAlt"),
    ("Data Sciences", "FaDatabase"),
    ("Supply", "FaTruck"),
    ("Quality", "FaClipboardCheck"),
    ("Vendor Strategy", "FaHandshake"),
]

def FocusGrid():
    return rx.vstack(
        rx.heading("Areas of Focus", size="xl", color="gray.800"),
        rx.grid(
            *[
                rx.box(
                    rx.vstack(
                        rx.icon(name=icon, font_size="2xl"),
                        rx.text(name, font_size="md", font_weight="semibold"),
                        rx.progress(value=75, size="sm"),  # placeholder %
                        rx.button("Go to dashboard", size="sm", on_click=lambda n=name: None),
                    ),
                    padding="1rem",
                    border="1px solid gray.200",
                    border_radius="md",
                    _hover={"boxShadow": "md"},
                    text_align="center",
                )
                for name, icon in functions
            ],
            # responsive columns: 1 col on mobile, up to 4 on desktop
            template_columns_responsive=["1fr", "1fr 1fr", "1fr 1fr 1fr 1fr"],
            gap="1.5rem",
        ),
    )
