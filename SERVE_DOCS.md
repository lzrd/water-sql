# Serving Documentation for Testing

When iterating on documentation, you can serve the HTML files from your computer to your student's browser over the network.

## Quick Start

```bash
# Build the package first (to generate HTML files)
./build.sh

# Serve the documentation
python3 serve_docs.py
```

The script will display URLs like:

```
====================================================================
📡 Documentation Server Started!
====================================================================

Serving files from: /home/user/water-sql/build/package

🌐 URLs to access the documentation:

  Local (this computer):
    http://localhost:8000/QUICKSTART.html
    http://localhost:8000/README.html

  Share with student (on same network):
    http://192.168.1.100:8000/QUICKSTART.html
    http://192.168.1.100:8000/README.html

💡 Tip: Send your student the '192.168.1.100' URL above

⚠️  Press Ctrl+C to stop the server
====================================================================
```

Send your student the "Share with student" URL.

## Custom Port or Directory

```bash
# Use a different port
python3 serve_docs.py 8080

# Serve a different directory
python3 serve_docs.py 8080 dist/package

# Test templates directly (without building)
cd src/templates
python3 ../../serve_docs.py 9000 .
```

## Testing Workflow

1. **Edit documentation** in `src/templates/*.md`
2. **Convert to HTML** without full build:
   ```bash
   cd build/package  # Or wherever you're serving from
   python3 ../../src/convert_md_to_html.py ../../src/templates/QUICKSTART.md
   ```
3. **Student refreshes browser** to see changes instantly
4. **Iterate** until documentation is clear

No need to rebuild the entire package or extract archives!

## Requirements

- Python 3 (no additional packages needed)
- Both computers on same network (or same computer for local testing)
- Firewall may need to allow incoming connections on the port

## Notes

- HTML files use relative links, so they work both:
  - Served via HTTP: `http://localhost:8000/QUICKSTART.html`
  - Opened locally: `file:///path/to/QUICKSTART.html`
- The server only logs errors (4xx, 5xx), not every request
- Press Ctrl+C to stop the server
