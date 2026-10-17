#!/usr/bin/env python3
"""Generate every Dartic icon (web, iOS, Android) from one vector mark.

The mark is a geometric "D" followed by a text cursor: typing Dart.

    python3 branding/build_icons.py

Needs Google Chrome (to rasterise the SVGs) and Pillow. The SVG masters are
written to branding/ so they can be opened in any design tool.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "branding"
WEB = ROOT / "landing_page"
APP = ROOT / "mobile"

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

# ── Palette ──────────────────────────────────────────────────
BG_TOP = "#1A1F27"
BG_BOTTOM = "#0B0D11"
BG_FLAT = "#111419"  # Android adaptive background / splash colour
INK = "#F4F3EE"      # the "D"
CURSOR = "#3D8BFF"   # the caret

# ── Geometry (1024 × 1024 canvas) ────────────────────────────
# "D": stem 150 wide, bowl 140 thick, 524 tall. Caret: 84 wide, 70 gap.
D_LEFT, TOP, BOTTOM = 179, 250, 774
STEM, BOWL = 150, 140
CARET_X, CARET_W = 761, 84


def mark(scale: float = 1.0, mono: str | None = None) -> str:
    """The D + caret mark, scaled around the canvas centre."""
    h = BOTTOM - TOP
    r_out = h / 2
    cx = D_LEFT + STEM + 100  # arc centre: a short flat run, then the bowl (right edge at 691)
    r_in = r_out - BOWL
    d = (
        f"M{D_LEFT} {TOP}H{cx}A{r_out} {r_out} 0 0 1 {cx} {BOTTOM}H{D_LEFT}Z"
        f"M{D_LEFT + STEM} {TOP + BOWL}H{cx}A{r_in} {r_in} 0 0 1 {cx} {BOTTOM - BOWL}H{D_LEFT + STEM}Z"
    )
    ink = mono or INK
    caret = mono or CURSOR
    t = f"translate({512 * (1 - scale)} {512 * (1 - scale)}) scale({scale})"
    return (
        f'<g transform="{t}">'
        f'<path d="{d}" fill="{ink}" fill-rule="evenodd"/>'
        f'<rect x="{CARET_X}" y="{TOP}" width="{CARET_W}" height="{h}" rx="6" fill="{caret}"/>'
        f"</g>"
    )


def background(radius: int = 0) -> str:
    return (
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>'
        "</linearGradient></defs>"
        f'<rect width="1024" height="1024" rx="{radius}" fill="url(#bg)"/>'
        # hairline highlight on the top edge for a bit of depth
        f'<rect x="1" y="1" width="1022" height="1022" rx="{max(radius - 1, 0)}" fill="none" '
        'stroke="#FFFFFF" stroke-opacity="0.06" stroke-width="2"/>'
    )


def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
        f'viewBox="0 0 1024 1024">{body}</svg>\n'
    )


# Variants ----------------------------------------------------
# The mark sits slightly left of centre (it is wider on the left), so shift it
# by its own optical centre: total width = 845 - 179 = 666 → centre 512. Good.
SQUARE = svg(background(0) + mark(0.92))           # iOS / maskable: OS applies the mask
ROUNDED = svg(background(232) + mark(0.92))        # web + legacy Android: pre-rounded
FAVICON = svg(background(232) + mark(1.08))        # bigger mark for 16–48 px
FOREGROUND = svg(mark(0.64))                       # Android adaptive layer (108dp, 66dp safe zone)
MONOCHROME = svg(mark(0.64, mono="#FFFFFF"))       # Android 13 themed icon
LAUNCH = svg(mark(0.9))                            # splash bitmap on a flat background


def rasterise(source: str, name: str, workdir: Path) -> Image.Image:
    path = workdir / f"{name}.svg"
    path.write_text(source)
    html = workdir / f"{name}.html"
    html.write_text(
        "<!doctype html><style>html,body{margin:0;background:transparent}"
        "img{display:block;width:1024px;height:1024px}</style>"
        f'<img src="{path.name}">'
    )
    png = workdir / f"{name}.png"
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--user-data-dir={workdir / 'chrome'}", "--window-size=1024,1024",
        "--default-background-color=00000000", "--force-device-scale-factor=2",
        f"--screenshot={png}", html.as_uri(),
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Chrome sometimes lingers after writing the screenshot; don't wait on it.
    for _ in range(300):
        if png.exists() and png.stat().st_size > 0:
            break
        try:
            proc.wait(timeout=0.1)
        except subprocess.TimeoutExpired:
            pass
    else:
        proc.kill()
        sys.exit(f"Chrome did not render {name}")
    proc.kill()
    img = Image.open(png).convert("RGBA")
    return img.resize((1024, 1024), Image.LANCZOS) if img.size != (1024, 1024) else img


def save(img: Image.Image, size: int, dest: Path, opaque: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    out = img.resize((size, size), Image.LANCZOS)
    if opaque:  # App Store rejects icons with an alpha channel
        flat = Image.new("RGB", out.size, BG_BOTTOM)
        flat.paste(out, mask=out.split()[3])
        out = flat
    out.save(dest, optimize=True)
    print(f"  {dest.relative_to(ROOT)}  {size}px")


def main() -> None:
    BRAND.mkdir(exist_ok=True)
    for name, src in [("icon-square", SQUARE), ("icon-rounded", ROUNDED), ("icon-favicon", FAVICON),
                      ("android-foreground", FOREGROUND), ("android-monochrome", MONOCHROME)]:
        (BRAND / f"{name}.svg").write_text(src)

    work = Path(tempfile.mkdtemp())
    try:
        sq = rasterise(SQUARE, "square", work)
        rd = rasterise(ROUNDED, "rounded", work)
        fv = rasterise(FAVICON, "favicon", work)
        fg = rasterise(FOREGROUND, "foreground", work)
        mo = rasterise(MONOCHROME, "monochrome", work)
        ln = rasterise(LAUNCH, "launch", work)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    sq.convert("RGB").save(BRAND / "icon-1024.png", optimize=True)

    print("Web (landing_page)")
    (WEB / "favicon.svg").write_text(FAVICON)
    fv.save(WEB / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  landing_page/favicon.ico  16/32/48px")
    img_dir = WEB / "assets" / "img"
    for s in (32, 64, 192, 512):
        save(fv if s <= 64 else rd, s, img_dir / f"icon-{s}.png")
    save(sq, 180, img_dir / "apple-touch-icon.png", opaque=True)
    save(sq, 512, img_dir / "icon-maskable-512.png", opaque=True)
    (img_dir / "icon-180.png").unlink(missing_ok=True)

    print("Flutter web (mobile/web)")
    save(fv, 64, APP / "web" / "favicon.png")
    save(rd, 192, APP / "web" / "icons" / "Icon-192.png")
    save(rd, 512, APP / "web" / "icons" / "Icon-512.png")
    save(sq, 192, APP / "web" / "icons" / "Icon-maskable-192.png", opaque=True)
    save(sq, 512, APP / "web" / "icons" / "Icon-maskable-512.png", opaque=True)

    print("In-app logo (onboarding)")
    save(rd, 512, APP / "assets" / "pngs" / "dartic.png")

    print("iOS (AppIcon.appiconset)")
    appicon = APP / "ios" / "Runner" / "Assets.xcassets" / "AppIcon.appiconset"
    sizes = {int(i["expected-size"]) for i in json.loads((appicon / "Contents.json").read_text())["images"]}
    for s in sorted(sizes):
        save(sq, s, appicon / f"{s}.png", opaque=True)

    print("iOS launch screen (LaunchImage.imageset, 131pt)")
    launch_set = appicon.parent / "LaunchImage.imageset"
    for f in launch_set.glob("*.png"):
        f.unlink()
    images = []
    for scale in (1, 2, 3):
        name = "LaunchImage.png" if scale == 1 else f"LaunchImage@{scale}x.png"
        save(ln, 131 * scale, launch_set / name)
        images.append({"filename": name, "idiom": "universal", "scale": f"{scale}x"})
    (launch_set / "Contents.json").write_text(
        json.dumps({"images": images, "info": {"author": "xcode", "version": 1}}, indent=2) + "\n"
    )

    print("Android")
    res = APP / "android" / "app" / "src" / "main" / "res"
    densities = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
    for d, k in densities.items():
        save(rd, round(48 * k), res / f"mipmap-{d}" / "ic_launcher.png")              # legacy (< API 26)
        save(fg, round(108 * k), res / f"mipmap-{d}" / "ic_launcher_foreground.png")  # adaptive layer
        save(mo, round(108 * k), res / f"mipmap-{d}" / "ic_launcher_monochrome.png")  # themed icon
        save(ln, round(96 * k), res / f"mipmap-{d}" / "launch_image.png")             # splash bitmap
    anydpi = res / "mipmap-anydpi-v26"
    anydpi.mkdir(exist_ok=True)
    (anydpi / "ic_launcher.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
        '    <background android:drawable="@color/ic_launcher_background" />\n'
        '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n'
        '    <monochrome android:drawable="@mipmap/ic_launcher_monochrome" />\n'
        "</adaptive-icon>\n"
    )
    (res / "values" / "ic_launcher_background.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <color name="ic_launcher_background">{BG_FLAT}</color>\n</resources>\n'
    )
    print("  mipmap-anydpi-v26/ic_launcher.xml, values/ic_launcher_background.xml")


if __name__ == "__main__":
    main()
