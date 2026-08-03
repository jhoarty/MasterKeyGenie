"""Regenerate brand-mark, favicon, and icon from assets/logo.png."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LOGO = ASSETS / "logo.png"


def content_mask(arr: np.ndarray, thresh: int = 245) -> np.ndarray:
    return ~((arr[:, :, 0] > thresh) & (arr[:, :, 1] > thresh) & (arr[:, :, 2] > thresh))


def bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    ys = np.where(rows)[0]
    xs = np.where(cols)[0]
    return int(xs[0]), int(ys[0]), int(xs[-1]), int(ys[-1])


def find_mark_bottom(row_counts: np.ndarray, r0: int, r1: int) -> int:
    kernel = 5
    smooth = np.convolve(row_counts.astype(float), np.ones(kernel) / kernel, mode="same")
    upper = smooth[r0 : r0 + int((r1 - r0) * 0.7)]
    peak_y = r0 + int(np.argmax(upper))
    peak_val = float(upper.max())
    threshold = max(8.0, peak_val * 0.02)

    y = peak_y
    while y <= r1:
        if smooth[y] < threshold:
            start = y
            while y <= r1 and smooth[y] < threshold:
                y += 1
            if y - start >= 12:
                return start - 1
        else:
            y += 1
    return r0 + int((r1 - r0) * 0.62)


def background_mask_flood(arr: np.ndarray, thresh: int = 248) -> np.ndarray:
    """True where pixels are background (near-white reachable from image edges).

    Preserves interior whites (e.g. the genie face) that are enclosed by color.
    """
    h, w = arr.shape[:2]
    near_white = (arr[:, :, 0] >= thresh) & (arr[:, :, 1] >= thresh) & (arr[:, :, 2] >= thresh)
    bg = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def try_push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and near_white[y, x] and not bg[y, x]:
            bg[y, x] = True
            q.append((y, x))

    for x in range(w):
        try_push(0, x)
        try_push(h - 1, x)
    for y in range(h):
        try_push(y, 0)
        try_push(y, w - 1)

    while q:
        y, x = q.popleft()
        try_push(y - 1, x)
        try_push(y + 1, x)
        try_push(y, x - 1)
        try_push(y, x + 1)

    return bg


def dilate(mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    out = mask.copy()
    for _ in range(iterations):
        padded = np.pad(out, 1, mode="constant", constant_values=False)
        neigh = (
            padded[:-2, 1:-1]
            | padded[2:, 1:-1]
            | padded[1:-1, :-2]
            | padded[1:-1, 2:]
            | padded[:-2, :-2]
            | padded[:-2, 2:]
            | padded[2:, :-2]
            | padded[2:, 2:]
        )
        out = out | neigh
    return out


def to_rgba_knockout_bg(im: Image.Image, thresh: int = 248) -> Image.Image:
    rgb = im.convert("RGB")
    arr = np.array(rgb)
    bg = background_mask_flood(arr, thresh=thresh)

    alpha = np.full((arr.shape[0], arr.shape[1]), 255, dtype=np.uint8)
    alpha[bg] = 0

    # Feather only anti-aliased edge pixels that touch the background —
    # never interior whites like the genie face.
    min_channel = arr.min(axis=2).astype(np.int16)
    edge_band = dilate(bg, iterations=2) & ~bg
    fringe = edge_band & (min_channel >= 230)
    fringe_alpha = np.clip((255 - min_channel) * (255 / 25), 0, 255).astype(np.uint8)
    alpha = np.where(fringe, np.minimum(alpha, fringe_alpha), alpha)

    rgba = np.dstack([arr, alpha])
    return Image.fromarray(rgba, "RGBA")


def make_square(rgba: Image.Image, size: int, pad_ratio: float = 0.08) -> Image.Image:
    arr = np.array(rgba)
    alpha = arr[:, :, 3] > 8
    if not np.any(alpha):
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))

    x0, y0, x1, y1 = bbox(alpha)
    cropped = rgba.crop((x0, y0, x1 + 1, y1 + 1))
    cw, ch = cropped.size
    max_side = max(cw, ch)
    pad = int(max_side * pad_ratio)
    canvas_side = max_side + pad * 2
    canvas = Image.new("RGBA", (canvas_side, canvas_side), (0, 0, 0, 0))
    ox = (canvas_side - cw) // 2
    oy = (canvas_side - ch) // 2
    canvas.paste(cropped, (ox, oy), cropped)
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    logo = Image.open(LOGO).convert("RGB")
    arr = np.array(logo)
    mask = content_mask(arr)
    c0, r0, c1, r1 = bbox(mask)
    row_counts = mask.sum(axis=1)
    mark_bottom = find_mark_bottom(row_counts, r0, r1)

    print(f"logo size: {logo.size}")
    print(f"content bbox: x={c0}-{c1}, y={r0}-{r1}")
    print(f"mark bottom row: {mark_bottom}")

    mark_mask = mask[r0 : mark_bottom + 1, :]
    cols = np.any(mark_mask, axis=0)
    xs = np.where(cols)[0]
    mx0, mx1 = int(xs[0]), int(xs[-1])

    pad = 8
    crop_box = (
        max(0, mx0 - pad),
        max(0, r0 - pad),
        min(logo.width, mx1 + 1 + pad),
        min(logo.height, mark_bottom + 1 + pad),
    )
    mark_rgb = logo.crop(crop_box)
    print(f"mark crop: {crop_box} -> {mark_rgb.size}")

    mark_rgba = to_rgba_knockout_bg(mark_rgb)

    brand = make_square(mark_rgba, 1024, pad_ratio=0.06)
    brand_path = ASSETS / "brand-mark.png"
    brand.save(brand_path, optimize=True)
    print(f"wrote {brand_path} {brand.size}")

    icon_mark = make_square(mark_rgba, 900, pad_ratio=0.04)
    icon = Image.new("RGBA", (1024, 1024), (255, 255, 255, 255))
    ox = (1024 - icon_mark.width) // 2
    oy = (1024 - icon_mark.height) // 2
    icon.paste(icon_mark, (ox, oy), icon_mark)
    icon_path = ASSETS / "icon.png"
    icon.convert("RGB").save(icon_path, optimize=True)
    print(f"wrote {icon_path} {icon.size}")

    fav = make_square(mark_rgba, 96, pad_ratio=0.05)
    fav_path = ASSETS / "favicon.png"
    fav.save(fav_path, optimize=True)
    print(f"wrote {fav_path} {fav.size}")

    preview = ASSETS / "_mark-crop-preview.png"
    # Checkerboard-style preview on mid gray so white face is visible
    prev = Image.new("RGBA", mark_rgba.size, (180, 180, 180, 255))
    prev.paste(mark_rgba, (0, 0), mark_rgba)
    prev.convert("RGB").save(preview)
    print(f"wrote {preview} {prev.size}")


if __name__ == "__main__":
    main()
