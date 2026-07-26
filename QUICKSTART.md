# Quickstart

## 1. Install

**macOS**

    brew install poppler pango cairo gdk-pixbuf libffi
    pip3 install -r requirements.txt

**Ubuntu / Debian / WSL**

    sudo apt-get update
    sudo apt-get install -y poppler-utils libpango-1.0-0 libpangoft2-1.0-0 \
        libcairo2 libgdk-pixbuf-2.0-0 libffi-dev
    pip3 install -r requirements.txt

**Windows (native)** — WeasyPrint needs GTK. Easiest path is WSL and the
Ubuntu instructions above. If you insist on native, install the GTK3
runtime first, then `pip install -r requirements.txt`.

A venv is recommended:

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

## 2. Build

    python3 build_all.py

Writes `chem_x19a_mt3_instruction_sheet.pdf` (2 pages) and
`chem_x19a_mt3_info_sheet.pdf` (1 page). It regenerates `assets/` every
run, so you can delete that folder freely.

The build **fails loudly** if a change pushes either sheet over its page
limit — that assertion is the point, don't remove it.

## 3. Edit

Content lives in two files only:

- `qsection.md` — the 2-page instruction sheet, one `<div class="problem">`
  per numbered box
- `info_sheet.md` — the 1-page chapter reference

Everything else (CSS, column packing, page breaks) is machinery. Read
`README.md` before editing — there are four markup traps that fail
silently rather than erroring.

## 4. If it breaks

| symptom | cause |
|---|---|
| `AssertionError: wanted 2 pages, got 3` | content too long; shorten, or widen the font ladder in `build_all.py` |
| equation invisible on a black header | black-on-transparent PNG — see trap 3 in README |
| a table bleeds into the next column | `nowrap` overflow — see trap 4 and the verify snippet |
| columns collapse into one | blank line between `</div>` and `<div>` — trap 2 |
| garbled text around a `<` | write `&lt;` — trap 1 |
