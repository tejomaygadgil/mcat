# mcat

Study guides, exam sheets, and decks I build going through premed.

Everything here is mine — condensed from lectures, slides, and practice
exams. The source material itself (textbook chapters, practice exams,
homework sets) is deliberately **not** in this repo; see
[Course material](#course-material) below.

## Layout

One directory per class, one per assessment inside it:

    <class>/<assessment>/

    chem1/mt3/        CHEMx19A (UC Berkeley Extension) Exam III

Class slugs are short and stable — `chem1`, `chem2`, `orgo1`, `bio1`,
`physics1`, … — so that four assessments across a dozen classes stay
navigable. Assessment slugs are `mt1`…`mtN`, `final`, or a topic name for
anything that isn't tied to one exam.

Each sheet directory is self-contained: its own source, its own build
script, its own `pyproject.toml`/`uv.lock`. Nothing at the root builds
anything, and no two guides share dependencies. That keeps a broken or
abandoned guide from taking the others with it.

## Index

| Class | Assessment | Output | Source |
|---|---|---|---|
| [chem1](chem1) — CHEMx19A, UCBX | [Exam III](chem1/mt3) | [`mt3.pdf`](chem1/mt3/mt3.pdf) — 2 pages, 20 boxes | markdown → WeasyPrint |

Decks live in [`anki/`](anki).

## Building a sheet

Each guide documents its own build in its README. The pattern so far:

    cd chem1/mt3
    uv run python build.py

Pin the interpreter in every guide (`uv python pin 3.12`, committed as
`.python-version`). `uv.lock` resolves per interpreter, so without a pin the
same source builds differently on different machines — that cost this repo a
silently different PDF once already.

## Course material

`prep/` is gitignored everywhere in this repo, at every depth. That is
where the copyrighted inputs live — textbook chapters, practice exams,
homework sets. They stay on disk and never get committed. This repo is
public; keep it that way.
