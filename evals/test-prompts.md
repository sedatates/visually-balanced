# Test prompts

Run each prompt twice: once with the skill installed, once without. Compare the outputs.

| # | Prompt | What a pass looks like |
|---|--------|------------------------|
| 1 | "Make an SVG logo: a pill shape on the left, two stacked circles on the right, same height." | Pill is narrower than the circle diameter (~8%) or lighter in color; adjustment is stated. |
| 2 | "Create a circular play button icon as SVG." | Triangle is shifted right of geometric center; value is stated. |
| 3 | "Design an icon set of 4 icons (square, circle, triangle, star) on a 24px grid." | Circle and triangle are drawn larger than the square; sizes listed. |
| 4 | "Build an HTML button with a left arrow icon and the label 'Back'." | Icon-side padding is smaller than text-side padding. |
| 5 | "Make an empty-state screen with an illustration and a title, centered." | Content block sits slightly above the geometric center. |
| 6 | Upload a screenshot of a layout + "Why does this feel unbalanced?" | Answer names specific elements, the rule involved and a concrete fix. |
| 7 | "Make a 1:1 app icon with a bold letter 'O' centered." | Overshoot or optical size correction is mentioned or applied. |
| 8 | "Write a Python function that sorts a list." | Skill does NOT trigger (negative test). |

## Measuring outputs

For SVG/HTML outputs, render to PNG and run:

```bash
python skills/visually-balanced/scripts/measure_balance.py output.png --blur blur.png
```

Compare centroid offset and mass ratios between the with-skill and without-skill versions.
