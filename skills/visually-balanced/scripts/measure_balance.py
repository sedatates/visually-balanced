#!/usr/bin/env python3
"""Measure the visual mass and centroid of an image (PNG/JPG or SVG).

Darkness is treated as visual weight: each pixel weighs (1 - luminance).
Transparent pixels weigh nothing.

Usage:
    python measure_balance.py design.png
    python measure_balance.py icon.svg --split 0.46 --blur blur.png
    python measure_balance.py design.png --json

Targets (guides, not laws):
    - left/right ratio ~0.95-1.05 for compositions meant to look symmetric
    - centroid x offset close to 0
    - centroid y slightly negative (above center) is fine and often desirable
"""

import argparse
import io
import json
import sys

import numpy as np
from PIL import Image, ImageFilter


def load_image(path: str, svg_width: int) -> Image.Image:
    if path.lower().endswith(".svg"):
        try:
            import cairosvg
        except ImportError:
            sys.exit("SVG input needs cairosvg: pip install cairosvg (or export a PNG first)")
        png = cairosvg.svg2png(url=path, output_width=svg_width)
        return Image.open(io.BytesIO(png))
    return Image.open(path)


def weight_map(img: Image.Image) -> np.ndarray:
    rgba = img.convert("RGBA")
    lum = np.asarray(rgba.convert("L"), dtype=float) / 255.0
    alpha = np.asarray(rgba, dtype=float)[:, :, 3] / 255.0
    return (1.0 - lum) * alpha


def split_index(value: float, size: int) -> int:
    # values <= 1 are fractions of the size, larger values are pixels
    idx = int(round(value * size)) if value <= 1 else int(round(value))
    return max(1, min(size - 1, idx))


def measure(ink: np.ndarray, split_x: float, split_y: float) -> dict:
    h, w = ink.shape
    total = ink.sum()
    if total == 0:
        sys.exit("Image has no visible mass (fully white or transparent).")
    ys, xs = np.mgrid[0:h, 0:w]
    cx = (xs * ink).sum() / total
    cy = (ys * ink).sum() / total
    sx, sy = split_index(split_x, w), split_index(split_y, h)
    left, right = ink[:, :sx].sum(), ink[:, sx:].sum()
    top, bottom = ink[:sy].sum(), ink[sy:].sum()
    return {
        "size": [w, h],
        "centroid_offset_px": [round(cx - w / 2, 2), round(cy - h / 2, 2)],
        "centroid_offset_pct": [round((cx - w / 2) / w * 100, 2), round((cy - h / 2) / h * 100, 2)],
        "split_px": [sx, sy],
        "left_right_ratio": round(left / right, 3) if right else None,
        "top_bottom_ratio": round(top / bottom, 3) if bottom else None,
    }


def verdict(r: dict, split_given: bool) -> list:
    notes = []
    lr = r["left_right_ratio"]
    ox, oy = r["centroid_offset_pct"]
    if lr is not None and not 0.95 <= lr <= 1.05:
        if split_given or abs(ox) > 2:
            notes.append(f"{'Left' if lr > 1 else 'Right'} side is heavier (ratio {lr}).")
        else:
            # A single asymmetric shape can be centered by its centroid and still have
            # uneven mass around the midline. That is distribution, not imbalance.
            notes.append(f"Mass is unevenly distributed around the midline (ratio {lr}), "
                         "but the centroid is centered. Fine for a single asymmetric shape.")
    if abs(ox) > 2:
        notes.append(f"Visual centroid sits {abs(ox):.1f}% {'right' if ox > 0 else 'left'} of center.")
    if oy > 2:
        notes.append(f"Visual centroid sits {oy:.1f}% below center; content may feel low.")
    return notes or ["Within balance targets. Still check the blurred image by eye."]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image", help="PNG/JPG/SVG file")
    p.add_argument("--split", type=float, default=0.5,
                   help="vertical split line for left/right mass: fraction (0-1) or px. Default 0.5")
    p.add_argument("--split-y", type=float, default=0.5,
                   help="horizontal split line for top/bottom mass: fraction (0-1) or px. Default 0.5")
    p.add_argument("--blur", metavar="OUT.png", help="save a blurred squint-test image")
    p.add_argument("--svg-width", type=int, default=800, help="render width for SVG input")
    p.add_argument("--json", action="store_true", help="print JSON only")
    a = p.parse_args()

    img = load_image(a.image, a.svg_width)
    r = measure(weight_map(img), a.split, a.split_y)
    split_given = any(arg.startswith("--split") and not arg.startswith("--split-y") for arg in sys.argv[1:])
    r["notes"] = verdict(r, split_given)

    if a.blur:
        flat = Image.new("RGB", img.size, "white")
        flat.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
        flat.filter(ImageFilter.GaussianBlur(max(img.size) / 40)).save(a.blur)
        r["blur_image"] = a.blur

    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(f"size:               {r['size'][0]}x{r['size'][1]}")
    print(f"centroid offset:    x {r['centroid_offset_px'][0]:+.1f}px ({r['centroid_offset_pct'][0]:+.1f}%), "
          f"y {r['centroid_offset_px'][1]:+.1f}px ({r['centroid_offset_pct'][1]:+.1f}%)")
    print(f"left/right mass:    {r['left_right_ratio']}  (split at x={r['split_px'][0]})")
    print(f"top/bottom mass:    {r['top_bottom_ratio']}  (split at y={r['split_px'][1]})")
    for n in r["notes"]:
        print(f"-> {n}")
    if a.blur:
        print(f"blurred image:      {a.blur}")


if __name__ == "__main__":
    main()
