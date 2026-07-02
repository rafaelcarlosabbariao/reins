"""Capture README screenshots from the running REINS dev server (localhost:3000).

Usage: python scripts/shots.py   (with the reflex app running)
Writes PNGs into docs/assets/.
"""
import glob
import os
import pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:3000"


def _chrome() -> str | None:
    """Prefer a cached playwright headless shell; fall back to bundled resolution."""
    cache = os.path.expanduser("~/Library/Caches/ms-playwright")
    hits = sorted(glob.glob(f"{cache}/chromium_headless_shell-*/*/chrome-headless-shell"))
    return hits[-1] if hits else None


def run():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=_chrome())
        pg = b.new_page(viewport={"width": 1440, "height": 900})

        # Home
        pg.goto(BASE, wait_until="networkidle")
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(OUT / "home.png"))

        # Portfolio — select a trial to reveal the resource analytics + donuts
        pg.goto(f"{BASE}/portfolio", wait_until="networkidle")
        pg.wait_for_timeout(2500)
        pg.get_by_text("ONCR-101 Phase II Efficacy Study", exact=True).first.click()
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(OUT / "dashboard.png"))
        # a tighter crop of just the analytics panel for the second README image
        panel = pg.get_by_text("Resource Analytics:").first
        box = panel.bounding_box()
        if box:
            pg.screenshot(
                path=str(OUT / "functional_breakdown.png"),
                clip={"x": box["x"] - 8, "y": box["y"] - 12, "width": 820, "height": 560},
            )

        # Resources
        pg.goto(f"{BASE}/resources", wait_until="networkidle")
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(OUT / "resources_panel.png"))

        b.close()
    for f in ("home.png", "dashboard.png", "functional_breakdown.png", "resources_panel.png"):
        pth = OUT / f
        print(f"{'✓' if pth.exists() else '✗'} {f} ({pth.stat().st_size if pth.exists() else 0} bytes)")


if __name__ == "__main__":
    run()
