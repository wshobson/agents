# claude-agents marketplace — multi-harness build & adapters
# ==========================================================
#
# All Python tooling runs through `uv`. No `pip`, no `requirements.txt`.
#
# Two uv-managed projects live in this repo:
#   - plugins/plugin-eval/        — adapter framework + plugin-eval suite
#                                   (extra-paths config makes tools/adapters/* importable)
#   - tools/yt-design-extractor/  — standalone YouTube extractor (heavy + optional)

GENERATE := tools/generate.py
EVAL_PROJECT := --project plugins/plugin-eval
YTX_DIR := tools/yt-design-extractor
YTX_SCRIPT := yt-design-extractor.py

# `uv run` against the plugin-eval venv — has pyyaml + extra-paths to tools/adapters/
UV_TOOLS := uv run $(EVAL_PROJECT) python

.PHONY: help install install-ocr install-easyocr deps check run run-full run-ocr run-transcript clean generate generate-all clean-generated install-opencode uninstall-opencode install-copilot uninstall-copilot validate garden test smoke-test generate-plugin sync-commands generate-all-commands clean-commands

help:
	@echo "claude-agents — multi-harness plugin marketplace"
	@echo "================================================="
	@echo ""
	@echo "Multi-harness adapter (Codex / Cursor / OpenCode / Gemini):"
	@echo "  make generate HARNESS=<h> [PLUGIN=<p>]           Generate per-harness artifacts (defaults to all plugins)"
	@echo "  make generate-all                                Generate for ALL harnesses + ALL plugins"
	@echo "  make clean-generated [HARNESS=<h>]               Remove generated artifacts"
	@echo "  make install-opencode [FORCE=1]                  Symlink OpenCode artifacts into global config"
	@echo "  make uninstall-opencode                          Remove repo-owned OpenCode symlinks"
	@echo "  make install-copilot [FORCE=1]                   Symlink Copilot artifacts into global config"
	@echo "  make uninstall-copilot                           Remove repo-owned Copilot symlinks"
	@echo "  make validate [HARNESS=<h>] [STRICT=1]           Structural validation of generated artifacts"
	@echo "  make garden [STRICT=1]                           Run doc-gardener (drift detection)"
	@echo "  make test                                        Full pytest suite (plugin-eval + tools)"
	@echo "  make smoke-test                                  Real-CLI smoke test (skips CLIs not on PATH)"
	@echo ""
	@echo "Legacy Gemini CLI targets (kept for compatibility — wrap make generate):"
	@echo "  make generate-plugin PLUGIN=<name>  Generate Gemini commands for one plugin"
	@echo "  make sync-commands                  Keep Gemini commands in sync"
	@echo "  make generate-all-commands          Generate Gemini commands for ALL plugins"
	@echo ""
	@echo "YouTube Design Extractor Setup (run in order):"
	@echo "  make install-ocr     Install system tools (tesseract + ffmpeg)"
	@echo "  make install         Install Python dependencies via uv"
	@echo "  make deps            Show what's installed"
	@echo ""
	@echo "Optional:"
	@echo "  make install-easyocr Install EasyOCR + PyTorch (~2GB, for stylized text)"
	@echo ""
	@echo "Usage (YouTube Extractor):"
	@echo "  make run URL=<youtube-url>           Basic extraction"
	@echo "  make run-full URL=<youtube-url>      Full extraction (OCR + colors + scene)"
	@echo "  make run-ocr URL=<youtube-url>       With OCR only"
	@echo "  make run-transcript URL=<youtube-url> Transcript + metadata only"
	@echo ""
	@echo "Examples:"
	@echo "  make run URL='https://youtu.be/eVnQFWGDEdY'"
	@echo "  make run-full URL='https://youtu.be/eVnQFWGDEdY' INTERVAL=15"
	@echo "  make generate-plugin PLUGIN=javascript-typescript"
	@echo ""
	@echo "Options (pass as make variables):"
	@echo "  URL=<url>          YouTube video URL (required)"
	@echo "  INTERVAL=<secs>    Frame interval in seconds (default: 30)"
	@echo "  OUTPUT=<dir>       Output directory"
	@echo "  ENGINE=<engine>    OCR engine: tesseract (default) or easyocr"

# Installation targets — yt-design-extractor uses its own uv project
install:
	cd $(YTX_DIR) && uv sync

install-ocr:
	@echo "Installing Tesseract OCR + ffmpeg..."
	@if command -v apt-get >/dev/null 2>&1; then \
		sudo apt-get update && sudo apt-get install -y tesseract-ocr ffmpeg; \
	elif command -v brew >/dev/null 2>&1; then \
		brew install tesseract ffmpeg; \
	elif command -v dnf >/dev/null 2>&1; then \
		sudo dnf install -y tesseract ffmpeg; \
	else \
		echo "Please install tesseract-ocr and ffmpeg manually"; \
		exit 1; \
	fi

install-easyocr:
	@echo "Installing PyTorch (CPU) + EasyOCR (~2GB download)..."
	cd $(YTX_DIR) && uv sync --extra easyocr

deps:
	@echo "Checking dependencies..."
	@echo ""
	@echo "System tools:"
	@command -v ffmpeg >/dev/null 2>&1 && echo "  ✓ ffmpeg" || echo "  ✗ ffmpeg (run: make install-ocr)"
	@command -v tesseract >/dev/null 2>&1 && echo "  ✓ tesseract" || echo "  ✗ tesseract (run: make install-ocr)"
	@echo ""
	@echo "Python packages (managed by uv in $(YTX_DIR)):"
	@cd $(YTX_DIR) && uv run python -c "import yt_dlp; print('  ✓ yt-dlp', yt_dlp.version.__version__)" 2>/dev/null || echo "  ✗ yt-dlp (run: make install)"
	@cd $(YTX_DIR) && uv run python -c "from youtube_transcript_api import YouTubeTranscriptApi; print('  ✓ youtube-transcript-api')" 2>/dev/null || echo "  ✗ youtube-transcript-api (run: make install)"
	@cd $(YTX_DIR) && uv run python -c "from PIL import Image; print('  ✓ Pillow')" 2>/dev/null || echo "  ✗ Pillow (run: make install)"
	@cd $(YTX_DIR) && uv run python -c "import pytesseract; print('  ✓ pytesseract')" 2>/dev/null || echo "  ✗ pytesseract (run: make install)"
	@cd $(YTX_DIR) && uv run python -c "from colorthief import ColorThief; print('  ✓ colorthief')" 2>/dev/null || echo "  ✗ colorthief (run: make install)"
	@echo ""
	@echo "Optional (for stylized text OCR):"
	@cd $(YTX_DIR) && uv run python -c "import easyocr; print('  ✓ easyocr')" 2>/dev/null || echo "  ○ easyocr (run: make install-easyocr)"

check:
	@cd $(YTX_DIR) && uv run python $(YTX_SCRIPT) --help >/dev/null && echo "✓ Script is working" || echo "✗ Script failed"

# Run targets
INTERVAL ?= 30
ENGINE ?= tesseract
OUTPUT ?=

run:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	cd $(YTX_DIR) && uv run python $(YTX_SCRIPT) '$(URL)' --interval '$(INTERVAL)' $(if $(OUTPUT),-o '$(OUTPUT)')

run-full:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-full URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	cd $(YTX_DIR) && uv run python $(YTX_SCRIPT) '$(URL)' --full --interval '$(INTERVAL)' --ocr-engine '$(ENGINE)' $(if $(OUTPUT),-o '$(OUTPUT)')

run-ocr:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-ocr URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	cd $(YTX_DIR) && uv run python $(YTX_SCRIPT) '$(URL)' --ocr --interval '$(INTERVAL)' --ocr-engine '$(ENGINE)' $(if $(OUTPUT),-o '$(OUTPUT)')

run-transcript:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-transcript URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	cd $(YTX_DIR) && uv run python $(YTX_SCRIPT) '$(URL)' --transcript-only $(if $(OUTPUT),-o '$(OUTPUT)')

# Cleanup
clean:
	rm -rf yt-extract-*
	@echo "Cleaned up extraction directories"

# Multi-harness adapter targets
# =============================
#
# All scripts run through plugin-eval's uv venv — it has pyyaml + extra-paths to
# tools/adapters, so the adapter framework and its dependencies are managed in
# one place (plugins/plugin-eval/pyproject.toml + uv.lock).
#
# Usage:
#   make generate HARNESS=codex PLUGIN=javascript-typescript   # one plugin
#   make generate HARNESS=cursor                               # all plugins (default)
#   make generate-all
#   make clean-generated HARNESS=opencode

HARNESSES := codex copilot cursor gemini opencode

generate:
ifndef HARNESS
	@echo "Error: HARNESS is required (one of: $(HARNESSES))"
	@echo "Examples:"
	@echo "  make generate HARNESS=codex                       # all plugins"
	@echo "  make generate HARNESS=codex PLUGIN=python-development   # one plugin"
	@exit 1
endif
ifdef PLUGIN
	$(UV_TOOLS) $(GENERATE) --harness '$(HARNESS)' --plugin '$(PLUGIN)'
else
	$(UV_TOOLS) $(GENERATE) --harness '$(HARNESS)' --all
endif

generate-all:
	@for h in $(HARNESSES); do \
		echo "--- $$h ---"; \
		$(UV_TOOLS) $(GENERATE) --harness $$h --all || exit 1; \
	done

validate:
ifdef HARNESS
	$(UV_TOOLS) tools/validate_generated.py --harness '$(HARNESS)' $(if $(STRICT),--strict)
else
	$(UV_TOOLS) tools/validate_generated.py $(if $(STRICT),--strict)
endif

garden:
	$(UV_TOOLS) tools/doc_gardener.py $(if $(STRICT),--strict)

# Full pytest suite — plugin-eval framework + tools/ adapters/validators/gardener.
test:
	uv run $(EVAL_PROJECT) pytest -q plugins/plugin-eval/ tools/tests/

# Real-CLI smoke test. Generates artifacts (if not present), then invokes whichever
# of opencode / gemini / codex / claude are on PATH. Per-CLI tests skip gracefully
# when the binary is missing — so local devs only exercise what they have installed.
# CI installs OpenCode + Gemini + Codex and turns those skips into hard requirements.
smoke-test:
	@if [ ! -d .opencode ] || [ ! -d .codex ] || [ ! -d commands ]; then \
		echo "Generating harness artifacts first..."; \
		$(MAKE) generate-all; \
	fi
	uv run $(EVAL_PROJECT) pytest -v tools/tests/test_cli_smoke.py

clean-generated:
ifdef HARNESS
	$(UV_TOOLS) $(GENERATE) --harness '$(HARNESS)' --clean
else
	@for h in $(HARNESSES); do \
		$(UV_TOOLS) $(GENERATE) --harness $$h --clean; \
	done
endif

install-opencode:
	$(UV_TOOLS) $(GENERATE) --harness opencode --all --prune
	$(UV_TOOLS) tools/install_opencode.py install $(if $(filter 1 true TRUE yes YES,$(FORCE)),--force)

uninstall-opencode:
	$(UV_TOOLS) tools/install_opencode.py uninstall

install-copilot:
	$(UV_TOOLS) $(GENERATE) --harness copilot --all --prune
	$(UV_TOOLS) tools/install_copilot.py install $(if $(filter 1 true TRUE yes YES,$(FORCE)),--force)

uninstall-copilot:
	$(UV_TOOLS) tools/install_copilot.py uninstall

# Legacy Gemini wrappers (delegate to the unified CLI)
generate-plugin:
ifndef PLUGIN
	@echo "Error: PLUGIN is required (e.g., make generate-plugin PLUGIN=javascript-typescript)"
	@exit 1
endif
	$(UV_TOOLS) $(GENERATE) --harness gemini --plugin '$(PLUGIN)'

sync-commands:
	$(UV_TOOLS) $(GENERATE) --harness gemini --all --prune

generate-all-commands:
	$(UV_TOOLS) $(GENERATE) --harness gemini --all

clean-commands:
	-rm -rf commands/
	@echo "Cleaned up commands/ (top-level Gemini TOMLs)"
