# Building on the user's template

```bash
python3 scripts/build.py deck.json --template brand.potx -o out/
```

or in the spec (path relative to the spec file):

```json
"template": {"path": "brand.pptx", "layout_map": {"cover": "Title Slide", "section": "Section Header", "content": "Title Only"}}
```

## What is taken from the template

| From the template | How it is used |
|---|---|
| Slide size | kept (4:3, 16:9, custom) |
| Theme fonts | text uses theme references (`+mj` for titles, `+mn` for body), and fitting is measured with those fonts |
| Theme accent (accent 1) | the highlight color for charts, tables, numbers |
| Title Slide layout | cover: title and subtitle placeholders |
| Section Header layout | section dividers: title and body placeholders (the section number is prefixed to the title) |
| Title Only layout | every content slide; the title placeholder's position defines the title zone, the grid spans its width |
| Slide-number placeholder | cloned onto each slide, so numbers sit where the template puts them |
| Sample slides in the file | dropped; only layouts are used |
| East Asian theme font | kept; if empty and the deck is `ko`/`ja`, Malgun Gothic / Yu Gothic is filled in |

Neutral greys (rules, non-highlighted bars) stay the built-in greys so every brand keeps a single accent.

## How layouts are found

For each role the builder takes, in order: the name in `layout_map`; a layout whose type is `title` / `secHead` / `titleOnly`; a layout whose name contains "Title Slide" / "Section" / "Title Only". If there is no Title Only layout it uses the first layout with a title placeholder and removes the unused content placeholder from each slide. A wrong name in `layout_map` fails with the list of real names.

## Geometry

- Title zone = the content layout's title placeholder (insets included).
- Body = from 0.2 in below the title to just above the footer line, across the title's width.
- Footer line = the bottom of the template's slide-number placeholder when it sits in the bottom fifth of the slide, otherwise 0.3 in above the bottom edge.
- The source line ends before the slide-number placeholder when they share the bottom band.

## Limits (v1)

- Decorations drawn on the template's layouts (logos, bars) are not detected. If the body overlaps one, pick another layout with `layout_map` or move the logo in the template.
- Title sizes are set explicitly (28 pt shrinking to 24 pt) so titles always fit; the template's title color, alignment and font are kept.
- Only one master is used (the one holding the chosen layouts).
- Text is measured at single line spacing. A template whose text styles use line spacing above 100% can make text taller than measured: check the PNG preview.
- Supported files: `.pptx` and `.potx`. Save a macro-enabled template (`.potm`, `.pptm`) as `.potx` first.
- Complex brand templates (many masters, custom placeholder sets) are the Pro `brand-fit` scope.
