# Gemini CLI Extension - Setup and Usage
# =====================================

PYTHON := python3
PIP := pip3

.PHONY: help generate-plugin sync-commands generate-all-commands clean-commands

help:
	@echo "Gemini CLI Extension"
	@echo "===================="
	@echo ""
	@echo "Setup:"
	@echo "  make generate-plugin PLUGIN=<name>  Generate commands for one plugin"
	@echo "  make sync-commands                  Keep local commands in sync with upstream"
	@echo "  make generate-all-commands          Generate commands for ALL plugins"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make generate-plugin PLUGIN=javascript-typescript"
	@echo "  make generate-plugin PLUGIN=python-development"

# Gemini CLI Extension targets
GEMINI_GEN := tools/generate_gemini_commands.py

generate-plugin:
ifndef PLUGIN
	@echo "Error: PLUGIN is required (e.g., make generate-plugin PLUGIN=javascript-typescript)"
	@exit 1
endif
	$(PYTHON) $(GEMINI_GEN) --plugin "$(PLUGIN)"

sync-commands:
	$(PYTHON) $(GEMINI_GEN) --prune

generate-all-commands:
	$(PYTHON) $(GEMINI_GEN)

clean-commands:
	-find commands -name "*.toml" -delete 2>/dev/null || true
	@echo "Cleaned up generated Gemini commands"

