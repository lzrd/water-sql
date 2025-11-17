#!/usr/bin/env python3
"""
Enhanced Markdown to HTML converter with proper table support.
Uses Python markdown library for accurate conversion.
"""

import markdown
from pathlib import Path
import sys

def create_html_template(content, title, current_file):
    """Create HTML page with navigation and styling."""

    # Determine navigation links based on current file location
    current_path = Path(current_file).resolve()

    # Check if we're in a Documentation directory
    if current_path.parent.name == 'Documentation':
        # We're in Documentation folder, go up one level for root files
        readme_link = "../README.html"
        install_link = "../INSTALL.html"
        quickstart_link = "../QUICKSTART.html"
        interview_link = "../INTERVIEW_PREP.html"
        spatial_link = "../SPATIAL_ANALYSIS.html"
        water_data_link = "WATER_DATA.html"
        time_codes_link = "TIME_CODES.html"
    else:
        # We're in root folder
        readme_link = "README.html"
        install_link = "INSTALL.html"
        quickstart_link = "QUICKSTART.html"
        interview_link = "INTERVIEW_PREP.html"
        spatial_link = "SPATIAL_ANALYSIS.html"
        water_data_link = "Documentation/WATER_DATA.html"
        time_codes_link = "Documentation/TIME_CODES.html"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #34495e;
            margin-top: 35px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #546e7a;
            margin-top: 25px;
        }}
        h4 {{
            color: #78909c;
            margin-top: 20px;
        }}
        code {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 0.9em;
            color: #e83e8c;
        }}
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        pre code {{
            background-color: transparent;
            border: none;
            padding: 0;
            color: #333;
            font-size: 0.95em;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            border: 1px solid #dee2e6;
            padding: 10px 15px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e9ecef;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #2980b9;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        .nav {{
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            color: white;
            padding: 15px 25px;
            margin: -40px -40px 30px -40px;
            border-radius: 8px 8px 0 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .nav strong {{
            font-size: 1.1em;
            margin-right: 20px;
        }}
        .nav a {{
            color: #3498db;
            margin-right: 15px;
            padding: 5px 10px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }}
        .nav a:hover {{
            background-color: rgba(52, 152, 219, 0.2);
            text-decoration: none;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #666;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 0 5px 5px 0;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <strong>Washington State Water Quality Data</strong> |
            <a href="{readme_link}">README</a>
            <a href="{quickstart_link}">Quick Start</a>
            <a href="{install_link}">Install</a>
            <a href="{spatial_link}">Maps</a>
            <a href="{water_data_link}">Database Guide</a>
            <a href="{interview_link}">Interview Prep</a>
        </div>
        {content}
    </div>
</body>
</html>'''


def convert_markdown_file(md_file, output_dir=None):
    """Convert a markdown file to HTML with proper table support."""
    md_path = Path(md_file)

    if not md_path.exists():
        print(f"✗ File not found: {md_file}")
        return False

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML using markdown library
    # Enable extensions for tables, code blocks, etc.
    md = markdown.Markdown(extensions=[
        'tables',           # GitHub-style tables
        'fenced_code',      # ```code blocks```
        'codehilite',       # Syntax highlighting
        'nl2br',            # Newline to <br>
        'sane_lists',       # Better list handling
    ])

    html_content = md.convert(md_content)

    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / md_path.with_suffix('.html').name
    else:
        output_path = md_path.with_suffix('.html')

    # Get title from filename
    title = md_path.stem.replace('_', ' ').title()

    # Create full HTML page
    full_html = create_html_template(html_content, title, output_path)

    # Write HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✓ Created {output_path}")
    return True


def main():
    """Convert markdown file(s) to HTML."""
    import sys

    # If arguments provided, convert just those files
    if len(sys.argv) > 1:
        success_count = 0
        fail_count = 0

        for md_file in sys.argv[1:]:
            if convert_markdown_file(md_file):
                success_count += 1
            else:
                fail_count += 1

        return 0 if fail_count == 0 else 1

    # Otherwise, convert all files (legacy mode)
    print("Converting Markdown to HTML with proper table support...")
    print("="*60)

    files = [
        ('README.md', 'washington_water_data'),
        ('INSTALL.md', 'washington_water_data'),
        ('WATER_DATA.md', 'washington_water_data/Documentation'),
        ('TIME_CODES.md', 'washington_water_data/Documentation'),
    ]

    success_count = 0
    for md_file, output_dir in files:
        if convert_markdown_file(md_file, output_dir):
            success_count += 1

    print("="*60)
    print(f"✓ Converted {success_count}/{len(files)} files successfully!")

    if success_count == len(files):
        print("\n✓ All HTML files generated with:")
        print("  - Proper table rendering")
        print("  - Correct navigation links")
        print("  - Professional styling")
        return 0
    else:
        print(f"\n✗ {len(files) - success_count} files failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
