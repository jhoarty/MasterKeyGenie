"""Locate and replace old Genie marks in marketing screenshots."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "assets" / "screenshots"
MARK = ROOT / "assets" / "brand-mark.png"

# Manually tuned cover rects (x, y, w, h) after probing — overwritten by detect
# if detection succeeds with a reasonable size.
TARGETS = {
    "windows_homescreen.png": {
        "search": (0, 0, 220, 240),
        "pad": 8,
    },
    # Gutter brand sits near calc(50% - 14rem - 17rem), not the far-left edge.
    "windows_project_screen.png": {
        "search": (280, 70, 180, 230),
        "pad": 10,
    },
    "master_key_genie.png": {
        "search": (0, 0, 200, 240),
        "pad": 8,
    },
}


def brand_mask(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    white = (r > 240) & (g > 240) & (b > 240)
    blue = (b > r + 15) & (b > g) & (b > 70) & ~white
    navy = (b >= r) & (r < 90) & (b < 160) & ((r.astype(int) + g + b) < 280)
    gold = (r > 150) & (g > 90) & (g < 230) & (b < 110) & (r > g)
    # light blue outline / sparkles
    cyan = (b > 150) & (g > 120) & (r < 140) & (b > r + 30)
    return blue | navy | gold | cyan


def detect_bbox(im: Image.Image, search: tuple[int, int, int, int], pad: int):
    arr = np.array(im.convert("RGBA"))
    x, y, w, h = search
    roi = arr[y : y + h, x : x + w, :3]
    mask = brand_mask(roi)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    # Expand slightly and clamp
    gx0 = max(0, x + x0 - pad)
    gy0 = max(0, y + y0 - pad)
    gx1 = min(im.width - 1, x + x1 + pad)
    gy1 = min(im.height - 1, y + y1 + pad)
    return gx0, gy0, gx1 - gx0 + 1, gy1 - gy0 + 1


def sample_bg(im: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Sample a nearby background pixel just outside the mark."""
    arr = np.array(im.convert("RGBA"))
    x, y, w, h = box
    candidates = [
        (x + w + 4, y + 4),
        (x + w + 4, y + h // 2),
        (max(0, x - 4), y + 4),
        (x + 4, max(0, y - 4)),
    ]
    for cx, cy in candidates:
        if 0 <= cx < im.width and 0 <= cy < im.height:
            px = arr[cy, cx]
            # Prefer light surfaces
            if int(px[0]) > 200 and int(px[1]) > 200 and int(px[2]) > 200:
                return tuple(int(v) for v in px)
    # fallback surface
    return (248, 250, 252, 255)


def replace_mark(path: Path, search: tuple[int, int, int, int], pad: int, mark: Image.Image):
    im = Image.open(path).convert("RGBA")
    box = detect_bbox(im, search, pad)
    if box is None:
        raise SystemExit(f"Could not find old mark in {path.name}")
    x, y, w, h = box
    print(f"{path.name}: replace @ ({x},{y}) {w}x{h}")

    bg = sample_bg(im, box)
    # Cover old mark with background rectangle (slightly larger)
    cover = Image.new("RGBA", (w, h), bg)
    im.paste(cover, (x, y))

    # Fit new mark into the same box, contain, centered
    mark_rgba = mark.convert("RGBA")
    # Use the larger dimension so the turban mark fills similarly
    fitted = mark_rgba.copy()
    fitted.thumbnail((w, h), Image.Resampling.LANCZOS)
    px = x + (w - fitted.width) // 2
    py = y + (h - fitted.height) // 2
    im.alpha_composite(fitted, (px, py))
    im.convert("RGB").save(path, optimize=True)
    print(f"  wrote {path}")


def main():
    mark = Image.open(MARK)
    print("mark", mark.size, mark.mode)
    for name, cfg in TARGETS.items():
        replace_mark(SHOTS / name, cfg["search"], cfg["pad"], mark)


if __name__ == "__main__":
    main()
