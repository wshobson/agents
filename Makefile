# YouTube Design Extractor - Setup and Usage
# ==========================================

PYTHON := python3
PIP := pip3
SCRIPT := tools/yt-design-extractor.py

.PHONY: help install install-ocr install-easyocr deps check run run-full run-ocr run-transcript clean

help:
	@echo "YouTube Design Extractor"
	@echo "========================"
	@echo ""
	@echo "Setup (run in order):"
	@echo "  make install-ocr     Install system tools (tesseract + ffmpeg)"
	@echo "  make install         Install Python dependencies"
	@echo "  make deps            Show what's installed"
	@echo ""
	@echo "Optional:"
	@echo "  make install-easyocr Install EasyOCR + PyTorch (~2GB, for stylized text)"
	@echo ""
	@echo "Usage:"
	@echo "  make run URL=<youtube-url>           Basic extraction"
	@echo "  make run-full URL=<youtube-url>      Full extraction (OCR + colors + scene)"
	@echo "  make run-ocr URL=<youtube-url>       With OCR only"
	@echo "  make run-transcript URL=<youtube-url> Transcript + metadata only"
	@echo ""
	@echo "Examples:"
	@echo "  make run URL='https://youtu.be/eVnQFWGDEdY'"
	@echo "  make run-full URL='https://youtu.be/eVnQFWGDEdY' INTERVAL=15"
	@echo ""
	@echo "Options (pass as make variables):"
	@echo "  URL=<url>          YouTube video URL (required)"
	@echo "  INTERVAL=<secs>    Frame interval in seconds (default: 30)"
	@echo "  OUTPUT=<dir>       Output directory"
	@echo "  ENGINE=<engine>    OCR engine: tesseract (default) or easyocr"

# Installation targets
install:
	$(PIP) install -r tools/requirements.txt

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
	$(PIP) install torch torchvision --index-url https://download.pytorch.org/whl/cpu
	$(PIP) install easyocr

deps:
	@echo "Checking dependencies..."
	@echo ""
	@echo "System tools:"
	@command -v ffmpeg >/dev/null 2>&1 && echo "  ✓ ffmpeg" || echo "  ✗ ffmpeg (run: make install-ocr)"
	@command -v tesseract >/dev/null 2>&1 && echo "  ✓ tesseract" || echo "  ✗ tesseract (run: make install-ocr)"
	@echo ""
	@echo "Python packages (required):"
	@$(PYTHON) -c "import yt_dlp; print('  ✓ yt-dlp', yt_dlp.version.__version__)" 2>/dev/null || echo "  ✗ yt-dlp (run: make install)"
	@$(PYTHON) -c "from youtube_transcript_api import YouTubeTranscriptApi; print('  ✓ youtube-transcript-api')" 2>/dev/null || echo "  ✗ youtube-transcript-api (run: make install)"
	@$(PYTHON) -c "from PIL import Image; print('  ✓ Pillow')" 2>/dev/null || echo "  ✗ Pillow (run: make install)"
	@$(PYTHON) -c "import pytesseract; print('  ✓ pytesseract')" 2>/dev/null || echo "  ✗ pytesseract (run: make install)"
	@$(PYTHON) -c "from colorthief import ColorThief; print('  ✓ colorthief')" 2>/dev/null || echo "  ✗ colorthief (run: make install)"
	@echo ""
	@echo "Optional (for stylized text OCR):"
	@$(PYTHON) -c "import easyocr; print('  ✓ easyocr')" 2>/dev/null || echo "  ○ easyocr (run: make install-easyocr)"

check:
	@$(PYTHON) $(SCRIPT) --help >/dev/null && echo "✓ Script is working" || echo "✗ Script failed"

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
	$(PYTHON) $(SCRIPT) "$(URL)" --interval $(INTERVAL) $(if $(OUTPUT),-o $(OUTPUT))

run-full:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-full URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --full --interval $(INTERVAL) --ocr-engine $(ENGINE) $(if $(OUTPUT),-o $(OUTPUT))

run-ocr:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-ocr URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --ocr --interval $(INTERVAL) --ocr-engine $(ENGINE) $(if $(OUTPUT),-o $(OUTPUT))

run-transcript:
ifndef URL
	@echo "Error: URL is required"
	@echo "Usage: make run-transcript URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --transcript-only $(if $(OUTPUT),-o $(OUTPUT))

# Cleanup
clean:
	rm -rf yt-extract-*
	@echo "Cleaned up extraction directories"
