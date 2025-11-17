# Makefile for Water Quality Data Package
#
# Common targets:
#   make              - Build package with default settings
#   make serve        - Serve documentation for testing
#   make html         - Convert markdown to HTML
#   make clean        - Clean build artifacts
#
# Variables:
#   VERSION=1.3.3     - Package version (default: 1.3.3)
#   DB=washington     - Database/state name (default: washington)
#   PORT=8000         - Server port (default: 8000)

VERSION ?= 1.3.3
DB ?= washington
PORT ?= 8000

# Directories
BUILD_DIR = build/package
TEMPLATES_DIR = src/templates
DOCS_DIR = $(TEMPLATES_DIR)/Documentation

# Source files
MD_FILES = $(TEMPLATES_DIR)/README.md \
           $(TEMPLATES_DIR)/QUICKSTART.md \
           $(TEMPLATES_DIR)/INSTALL.md \
           $(TEMPLATES_DIR)/INTERVIEW_PREP.md \
           $(TEMPLATES_DIR)/SPATIAL_ANALYSIS.md \
           $(DOCS_DIR)/WATER_DATA.md \
           $(DOCS_DIR)/TIME_CODES.md

# Generated HTML files
HTML_FILES = $(BUILD_DIR)/README.html \
             $(BUILD_DIR)/QUICKSTART.html \
             $(BUILD_DIR)/INSTALL.html \
             $(BUILD_DIR)/INTERVIEW_PREP.html \
             $(BUILD_DIR)/SPATIAL_ANALYSIS.html \
             $(BUILD_DIR)/index.html \
             $(BUILD_DIR)/Documentation/WATER_DATA.html \
             $(BUILD_DIR)/Documentation/TIME_CODES.html

.PHONY: all build html serve clean help

# Default target
all: build

# Build the complete package
build:
	@echo "Building package: $(DB) version $(VERSION)"
	./build.sh $(DB) $(VERSION)

# Convert markdown to HTML (for quick iteration)
html: $(HTML_FILES)

# Special rule for index.html (already HTML, just copy)
$(BUILD_DIR)/index.html: $(TEMPLATES_DIR)/index.html
	@echo "Copying index.html..."
	@mkdir -p $(BUILD_DIR)
	@cp $< $@

# Pattern rule for root-level markdown files
$(BUILD_DIR)/%.html: $(TEMPLATES_DIR)/%.md
	@echo "Converting $< to HTML..."
	@mkdir -p $(BUILD_DIR)
	@cp $< $(BUILD_DIR)/
	@cd $(BUILD_DIR) && python3 ../../src/convert_md_to_html.py $(notdir $<)
	@rm $(BUILD_DIR)/$(notdir $<)

# Pattern rule for Documentation markdown files
$(BUILD_DIR)/Documentation/%.html: $(DOCS_DIR)/%.md
	@echo "Converting $< to HTML..."
	@mkdir -p $(BUILD_DIR)/Documentation
	@cp $< $(BUILD_DIR)/Documentation/
	@cd $(BUILD_DIR)/Documentation && python3 ../../../src/convert_md_to_html.py $(notdir $<)
	@rm $(BUILD_DIR)/Documentation/$(notdir $<)

# Serve documentation for testing (depends on HTML being generated)
serve: html
	@echo ""
	@echo "=========================================="
	@echo "Starting documentation server..."
	@echo "=========================================="
	@echo ""
	@echo "📝 HTML files available:"
	@echo "   - index.html (landing page - START HERE!)"
	@echo "   - README.html"
	@echo "   - QUICKSTART.html (with turbidity example!)"
	@echo "   - INSTALL.html"
	@echo "   - INTERVIEW_PREP.html"
	@echo "   - Documentation/WATER_DATA.html"
	@echo "   - Documentation/TIME_CODES.html"
	@echo ""
	@echo "🌐 Server will show URLs to share with students"
	@echo "💡 Share http://YOUR-IP:$(PORT)/ (or http://YOUR-IP:$(PORT)/index.html)"
	@echo ""
	python3 serve_docs.py $(PORT) $(BUILD_DIR)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/package
	rm -f dist/*.zip dist/*.tar.gz
	@echo "✓ Clean complete"

# Show help
help:
	@echo "Water Quality Data Package - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make [target] [VARIABLE=value]"
	@echo ""
	@echo "Targets:"
	@echo "  all (default)  - Build complete package"
	@echo "  build          - Build complete package"
	@echo "  html           - Convert markdown to HTML only"
	@echo "  serve          - Serve documentation on HTTP server"
	@echo "  clean          - Remove build artifacts"
	@echo "  help           - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  VERSION=1.3.3      - Package version (default: 1.3.3)"
	@echo "  DB=washington      - State/database name (default: washington)"
	@echo "  PORT=8000          - HTTP server port (default: 8000)"
	@echo ""
	@echo "Examples:"
	@echo "  make                           # Build with defaults"
	@echo "  make VERSION=2.0 DB=oregon     # Build Oregon v2.0"
	@echo "  make serve                     # Serve docs on port 8000"
	@echo "  make serve PORT=8080           # Serve docs on port 8080"
	@echo "  make html                      # Just convert MD to HTML"
	@echo "  make clean                     # Clean build directory"
	@echo ""
	@echo "Quick iteration workflow:"
	@echo "  1. Edit src/templates/QUICKSTART.md"
	@echo "  2. make html                   # Convert to HTML"
	@echo "  3. make serve                  # Start server (in another terminal)"
	@echo "  4. Student refreshes browser to see changes"
