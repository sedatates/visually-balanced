# visually-balanced

**An Agent Skill that teaches AI to design with optical balance, not just math.**

Equal numbers don't always look equal. The eye reads *mass* (area, darkness, complexity), not bounding boxes. This skill gives Claude (and other skill-compatible agents) the rules designers use to correct for that, plus a script that measures visual weight so the corrections can be checked.

![Math vs optical balance](examples/comparison.png)

| Example | Math | Optical fix | Measured |
|---|---|---|---|
| Pill + two circles | 100 / 100 width | 92 / 100 width | left/right mass 1.13 → 1.05 |
| Play icon in a circle | triangle box centered | shifted right by w/6 | centroid offset -5.6% → -0.2% |

## What's inside

```
skills/visually-balanced/
├── SKILL.md                  # 8 optical rules with starting values, workflow, review format
└── scripts/
    └── measure_balance.py    # visual centroid + mass ratios for PNG/JPG/SVG
examples/                     # SVGs used in the comparison above
evals/test-prompts.md         # with/without-skill test prompts
```

### The 8 rules
1. Equalize mass, not the bounding box
2. Overshoot round and pointed shapes
3. Center optically (asymmetric shapes, vertical center, directional icons)
4. The top half looks bigger
5. Horizontal strokes look thicker
6. Color and value carry weight
7. Complexity and isolation add weight
8. Optical padding in buttons and icon + text

## Install

**Claude Code**

```bash
git clone https://github.com/sedatates/visually-balanced.git
cp -r visually-balanced/skills/visually-balanced ~/.claude/skills/
```

Or copy it into a project's `.claude/skills/` folder to scope it to that project.

**Claude apps (claude.ai / desktop)**

Zip the `skills/visually-balanced` folder and upload it as a custom skill in Claude's settings.

**Other agents**

Any tool that supports the Agent Skills format (`SKILL.md` with `name` / `description` frontmatter) can load the folder as is.

## Using the measurement script

```bash
pip install pillow numpy cairosvg   # cairosvg only needed for SVG input

python skills/visually-balanced/scripts/measure_balance.py design.png
python skills/visually-balanced/scripts/measure_balance.py icon.svg --blur blur.png
python skills/visually-balanced/scripts/measure_balance.py layout.png --split 112 --json
```

Example output:

```
size:               240x240
centroid offset:    x -3.6px (-1.5%), y -0.5px (-0.2%)
left/right mass:    1.13  (split at x=120)
top/bottom mass:    1.0  (split at y=120)
-> Left side is heavier (ratio 1.13).
```

Numbers guide, eyes decide. Always check the blurred image too.

## Testing

See [`evals/test-prompts.md`](evals/test-prompts.md). Run each prompt with and without the skill and compare the outputs.

## License

MIT
