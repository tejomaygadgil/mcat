# CHEMx19A — Exam III sheet

`mt3.pdf` — 2 pages, 20 numbered boxes, one per study-guide question, built
from `qsection.md`.

    qsection.md   sheet source — the only file you edit
    build.py      figures, layout solver, PDF render
    assets/       generated images (wiped and rebuilt every run)
    prep/         course source material (untracked)

## Build

Needs [uv](https://docs.astral.sh/uv/) plus the **GTK** stack
pango/cairo/gdk-pixbuf, which `weasyprint` loads at runtime.

    # macOS
    brew install pango cairo gdk-pixbuf libffi
    # Ubuntu / Debian / WSL
    sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 \
        libgdk-pixbuf-2.0-0 libffi-dev

    uv run python build.py

`uv` installs the pinned dependencies from `uv.lock` into `.venv/` on first
run. On macOS the script re-execs itself once with
`DYLD_FALLBACK_LIBRARY_PATH` pointed at the Homebrew lib directory, because
dyld only reads that variable at process launch and WeasyPrint can't
otherwise find the GTK libraries.

`build.py` renders the LaTeX images, measures every box at the real column
width, splits them into columns at the `PINS` boundaries, then searches the
font ladder. It asserts the page count (2) and **fails loudly** if a change
pushes the sheet over — that assertion is the point, don't remove it.

## Editing

Edit content only in `qsection.md`. One `<div class="problem">` per box,
titled `#### (n) Description` where `n` is the study-guide question number.
Page and column breaks are computed, never hand-placed — don't add
`<!--pagebreak-->` or `<!--colbreak-->` yourself.

### Markup traps

1. A bare `<` before a letter is parsed as an HTML tag and silently
   corrupts the layout. Write `&lt;` — e.g. `s &lt; p &lt; d &lt; f`.
2. Adjacent divs need `</div>` on the line immediately before the next
   `<div ...>`, with no blank line between, or `md_in_html` emits an
   unbalanced tag and the columns collapse.
3. **Equation images are black text on transparent.** They vanish on the
   black `####` header bars. If you need one inside a header, add it to
   `EQ_WHITE` in `build.py` — that's why `s_zeff_w.png` exists.
4. **`white-space: nowrap` tables overflow instead of wrapping.** The
   `.emtable` and `.lut` classes set it, so a too-wide row silently bleeds
   past the column edge rather than failing the build. Column 1 ends at
   x=300.2pt, column 2 starts at 313.1pt (letter, 0.3in margins, 2 cols).

The build only asserts page count, not horizontal overflow. To check a table
actually fits:

    uv run python -c "
    import pdfplumber
    with pdfplumber.open('mt3.pdf') as pdf:
        pg = pdf.pages[0]
        bad = [w for w in pg.extract_words() if 300.2 < w['x1'] < 313.1]
        print('overflow:', [w['text'] for w in bad] or 'none')
    "

## Lookup-table convention

Boxes (1)-(3) are built as unit-pair lookup grids rather than procedures.
The corner cell names both axes (`λ ↓ ν →`), so units are stated once in
the headers instead of repeated in every row label. Constants are
pre-multiplied so a value can be plugged straight in with no unit
conversion step:

- (2) each cell is **c expressed in that unit pair**, so `λ × ν = cell`
  holds in both directions — divide the cell by whichever you have.
- (3) each cell is **hc** (or **h**) folded with the nm/mol conversions.

If you change a constant, re-verify it. Every cell in (2) and (3) was
checked against a 500 nm photon: 6.00×10¹⁴ Hz, 3.98×10⁻¹⁹ J, 240 kJ/mol.

## Numbering

The study guide's summary section resolves to 18 top-level MC topics, then
Lewis structures, then 4 word problems = 23 questions, matching its own
points table (Q1–18 @ 6.5, Q19 @ 26, Q20–23 @ 14/14/15/14 = 200). Several
share a box on the sheet, so the PDF has 20.

Beware: the `.docx` flattens all indent levels to identical dashes. Bullets
ending in `:` are headers owning the ones beneath them — counting every dash
as a topic gives 21 and does not match the exam.

## If it breaks

| symptom | cause |
|---|---|
| `nothing fits 2 pages` | content too long; shorten, or widen the font ladder (`PT_MIN`/`PT_START`) |
| equation invisible on a black header | black-on-transparent PNG — see trap 3 |
| a table bleeds into the next column | `nowrap` overflow — see trap 4 and the verify snippet |
| columns collapse into one | blank line between `</div>` and `<div>` — trap 2 |
| garbled text around a `<` | write `&lt;` — trap 1 |
