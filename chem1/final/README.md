# CHEMx19A — Final Exam sheet

`final.pdf` — 2 pages, 25 boxes covering all 29 exam questions, built from
`sheet.md`.

    sheet.md      sheet source — the only file you edit
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
run.

**`.python-version` is load-bearing — don't delete it.** Same reasoning as
mt3: `uv.lock` resolves per interpreter, and different WeasyPrint builds lay
text out differently, which changes the font-search result. Pinning collapses
the lock to one resolution so clean builds agree.

On macOS the script re-execs itself once with
`DYLD_FALLBACK_LIBRARY_PATH` pointed at the Homebrew lib directory, because
dyld only reads that variable at process launch and WeasyPrint can't
otherwise find the GTK libraries.

`build.py` renders the equation/diagram images, measures every box at the
real column width, splits them into **four balanced columns** (unlike mt3's
hand-pinned `PINS`, the cut points are solved by a small DP that minimizes
the tallest column — boxes stay in question order), then searches the font
ladder. It asserts the page count (2) and **fails loudly** if a change pushes
the sheet over — that assertion is the point, don't remove it.

Current build: 7.2pt, columns ~90/86/93/99% full. The five WORD boxes
(25)–(29) are a forced suffix — together they nearly fill their column, so
that is the binding constraint; new content is cheapest in boxes (1)–(14).

## Editing

Edit content only in `sheet.md`. One `<div class="problem">` per box, titled
`#### (n) Description` where `n` is the exam question number from the
final-exam summary. Page and column breaks are computed, never hand-placed.

### Markup traps

1. A bare `<` before a letter is parsed as an HTML tag and silently
   corrupts the layout. Write `&lt;` — e.g. `&lt;109.5°`.
2. Adjacent divs need `</div>` on the line immediately before the next
   `<div ...>`, with no blank line between, or `md_in_html` emits an
   unbalanced tag and the columns collapse.
3. A `*` after a bold span (`**σ and σ***`) is swallowed as an emphasis
   marker and italicizes the rest of the line. Escape it: `σ\*`.
4. A `-` bullet list directly after a numbered list with no blank line
   between them is absorbed into the last numbered item.

The build only asserts page count, not horizontal overflow. To check nothing
bleeds past a column edge (col 1 ends x=300.2pt, col 2 starts 313.1pt):

    uv run --with pdfplumber python -c "
    import pdfplumber
    with pdfplumber.open('final.pdf') as pdf:
        for pg in pdf.pages:
            bad = [w for w in pg.extract_words()
                   if 300.2 < w['x1'] < 313.1 or w['x1'] > 590.4]
            print('overflow:', [w['text'] for w in bad] or 'none')
    "

## Numbering

The final-exam summary lists 29 questions worth 300 pts: 24 MC (Q1–24 @ 8.5)
and 5 word problems (Q25–28 @ 19, Q29 @ 20). The MC split is Ch10 → Q1–8,
Ch11 → Q9–17, Ch12 → Q18–24, in the order the summary lists the topics.
Paired topics share a box, plus two unnumbered support boxes ported from
mt3: "Lewis Structures (Kelter)" leads the sheet — questions 1–8 all start
from a Lewis structure — and "Periodic Trends" follows (3–4), feeding the
dipole ranking, hydration, and dispersion answers. That makes 25 boxes.

Deliberately **excluded** (on the practice exam / HW but not among the
summary's 29 questions): unit-cell density/radius calculations,
Clausius–Clapeyron, fractional crystallization.

The exam hands out the periodic table and the VSEPR shape chart; box (1–2)
duplicates the VSEPR chart compactly anyway (with hybridization + polarity
columns) so questions 1–6 resolve from one table.

## Verification

Every worked example was checked against the practice-exam answer key
(q35 → 87.7 kJ, q36 → 67.7 kJ, q64 → 59 M/atm, q65 → 70.7 mmHg,
q66 → 17.0 mmHg, q69 → 2.7, q70 → ≈120 g/mol, q71 → 223 g/mol), and the MO
table against the key (q17 all of O₂/O₂⁺/O₂⁻ paramagnetic, q18 N₂⁺ & N₂⁻,
q19 Cl₂⁺ BO 1.5, q20 Cl₂⁻ BO 0.5).

n.b. the summary's own % w/v example ("1.5% × 250 mL = 31.25 g") contradicts
its stated formula; the sheet flags this and carries the formula-consistent
3.75 g.

## If it breaks

| symptom | cause |
|---|---|
| `nothing fits 2 pages` | content too long; shorten, or widen the font ladder (`PT_MIN`/`PT_START`) |
| a table bleeds into the next column | overflow — see the verify snippet |
| columns collapse into one | blank line between `</div>` and `<div>` — trap 2 |
| garbled text around a `<` | write `&lt;` — trap 1 |
| half a line unexpectedly italic | stray `*` after bold — trap 3 |
