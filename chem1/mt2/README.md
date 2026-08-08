# CHEMx19A — Exam II sheet

`mt2.pdf` — 2 pages covering solutions, gases, and thermodynamics, built
from `sheet.md`.

    sheet.md      sheet source — the only file you edit
    build.py      equation images + PDF render
    assets/       generated images (wiped and rebuilt every run)

Sections: Ch 4 Solutions (solubility, oxidation), Ch 5 Gas, Ch 6
Thermodynamics, Reaction Types, Polyatomic Ions.

## Build

Needs [uv](https://docs.astral.sh/uv/) plus the **GTK** stack
pango/cairo/gdk-pixbuf, which `weasyprint` loads at runtime.

    # macOS
    brew install pango cairo gdk-pixbuf libffi
    # Ubuntu / Debian / WSL
    sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 \
        libgdk-pixbuf-2.0-0 libffi-dev

    uv run python build.py

**`.python-version` is load-bearing — don't delete it.** `uv.lock` resolves
per interpreter, so without a pin the same source builds differently on
different machines. See the [Exam III sheet](../mt3) for the incident.

On macOS the script re-execs itself once with `DYLD_FALLBACK_LIBRARY_PATH`
pointed at the Homebrew lib directory, because dyld only reads that variable
at process launch and WeasyPrint can't otherwise find the GTK libraries.

## Editing

Edit content only in `sheet.md`.

Unlike the [Exam III sheet](../mt3), **breaks here are hand-placed.** This
sheet has no measuring pass, no column solver, and no font search — type
sizes are fixed in the CSS and you position `<!--colbreak-->` and
`<!--pagebreak-->` markers yourself. The layout is two pages of two columns
each, with page 2 set smaller via `.page:nth-child(2)`.

The build asserts the page count (2) and fails if a change pushes the sheet
over. When it does, move a break rather than reaching for a font size.

### Markup traps

1. A bare `<` before a letter is parsed as an HTML tag and silently
   corrupts the layout. Write `&lt;`.
2. Adjacent divs need `</div>` on the line immediately before the next
   `<div ...>`, with no blank line between, or `md_in_html` emits an
   unbalanced tag and the columns collapse.
3. Equation images are black text on transparent, so they disappear on any
   dark background. The `###` header bars are dark — keep equations out of
   them.

## Equations

`EQUATIONS` in `build.py` maps a name to a LaTeX string; every entry is
rendered to `assets/<name>.png` through matplotlib mathtext and referenced
from `sheet.md` as `<img src="assets/<name>.png" class="eq">`.

matplotlib sizes each PNG to its content, so a long equation would otherwise
set its own scale on the page. `EQ_WIDTH_PT` caps the width per image, in
points; anything not listed falls back to `EQ_MAX_WIDTH_PT`.
