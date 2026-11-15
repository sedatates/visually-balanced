---
name: visually-balanced
description: Apply optical (visual) balance corrections when designing or reviewing UI, icons, logos, buttons, layouts and SVG/HTML visuals. Use when elements must look balanced, centered or equal-sized, not just measure equal, or when a design "feels off".
---

# Visually Balanced

The eye perceives **mass (area × darkness × complexity)**, not bounding boxes. Geometrically equal is not visually equal. Build with math and a grid first, then correct optically. Math is the starting point; the eye is the final judge.

Use this skill when:
- Creating icons, logos, app icons, illustrations, SVG/CSS shapes
- Building buttons, chips, badges, nav bars, cards, icon + text combos
- Composing layouts with several shapes or elements side by side
- Reviewing a design (screenshot, Figma export, HTML) where something "feels off"

## Core rules (with starting values)

### 1. Equalize mass, not the bounding box
- Shapes in the same box look different sizes: the square looks biggest, the circle smaller, the triangle smallest.
- Equal-area circle diameter ≈ **1.13 × square side**. In practice use **~1.08–1.12×** (Material keylines: 18px square ↔ 20px circle on a 24px grid).
- Triangles and pointed shapes: enlarge **~1.15–1.25×** relative to a square.
- Continuous blocks (pills, rectangles) weigh more than separated shapes with gaps or pinch points. A pill next to two stacked circles of the same width carries ~13% more area; narrowing the pill ~8% (100 → 92) brings it close to equal.
- When unsure, compute the real filled area of each element and make them roughly equal.

### 2. Overshoot
- Round and pointed shapes must extend slightly past the baseline, cap line or container edge, otherwise they look smaller.
- Overshoot ≈ **1.5–3% of the height** (in type, "O" is taller than "H" and the apex of "A" rises past cap height).

### 3. Optical centering
- **Asymmetric shapes:** a right-pointing triangle's centroid sits w/6 (≈17% of its width) left of its box center. Shift it right somewhere between 0 and w/6; most play icons land at **~8–15% of the triangle's width**.
- **Vertical:** the true center reads as low. Place content **~2–5% above** the geometric center (posters, empty states, modals, hero blocks).
- **Directional icons** (arrows, chevrons): nudge slightly toward the direction they point.

### 4. The top half looks bigger
- Make the upper part of stacked forms slightly smaller ("S", "8", "B", stacked layouts).

### 5. Horizontal strokes look thicker
- Make horizontal strokes **~5–10% thinner** than vertical ones for equal perceived weight.

### 6. Color and value carry weight
- Dark, saturated, warm = heavy. Light, desaturated, cool = light.
- A lighter element can be slightly larger to balance a darker one; or lighten the heavier side. Shape and color corrections can be combined.

### 7. Complexity and isolation add weight
- Detailed or textured elements outweigh plain ones of the same size.
- An element alone in whitespace draws more attention than one inside a group.

### 8. Buttons and icon + text
- Icon side padding: reduce by **~2–4px** (or ~0.75×) compared with the text side.
- Text vertical centering: lowercase-heavy labels often need a **~1px upward** nudge; all-caps labels usually center cleanly.
- Icons inside circular buttons: apply rule 3 to asymmetric glyphs.

## Workflow

1. **Build with math:** grid, equal values, consistent spacing.
2. **Measure mass:** compare filled areas and visual weight, not widths.
3. **Correct optically:** apply the rules above; keep corrections small (usually 1–10%).
4. **Verify:**
   - Squint test or blur: which side leaves the darker, bigger blob?
   - Flip or mirror: imbalance becomes obvious once the eye loses familiarity.
   - For code-generated visuals, render and measure with the script below.
5. **Report** the adjustments with exact values (e.g. "pill width 100 → 92, play icon +6px right").

## Measuring (scripts/measure_balance.py)

Treats darkness as weight and reports the visual centroid and mass ratios. Accepts PNG/JPG, or SVG if `cairosvg` is installed.

```bash
python scripts/measure_balance.py design.png
python scripts/measure_balance.py icon.svg --blur blur.png        # also save a squint-test image
python scripts/measure_balance.py layout.png --split 112           # compare two groups split at x=112px
python scripts/measure_balance.py layout.png --json
```

- Use `--split` (fraction or px) to compare two groups that meet somewhere other than the midline.
- Targets: left/right ratio ~0.95–1.05 for compositions meant to look symmetric; centroid x near 0; centroid y slightly negative (above center) is fine.
- For a single asymmetric shape, trust the centroid, not the midline ratio.
- Numbers guide, eyes decide: always look at the blurred image too.

## Review output format

When reviewing a design, list each issue as:
- **Element**: what feels off, **why** (which rule), **fix** with a concrete value.

Keep it short and skip elements that already look balanced.
