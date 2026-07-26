# Build the exam sheets with uv.
#
# WeasyPrint loads native GTK libraries (pango/cairo/gdk-pixbuf) at runtime.
# On macOS these live under the Homebrew prefix and the venv Python can't find
# them without DYLD_FALLBACK_LIBRARY_PATH. We derive that path from `brew`
# (works on both Apple Silicon /opt/homebrew and Intel /usr/local); on Linux
# the libraries are on the default loader path and this is a no-op.
BREW_LIB := $(shell command -v brew >/dev/null 2>&1 && echo $$(brew --prefix)/lib)

.PHONY: build clean

build:
	DYLD_FALLBACK_LIBRARY_PATH=$(BREW_LIB) uv run python build_all.py

clean:
	rm -rf assets __pycache__
