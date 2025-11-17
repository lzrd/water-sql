#!/usr/bin/env python3
"""
Simple HTTP server for testing documentation

Usage:
    python3 serve_docs.py [port] [directory]

Examples:
    python3 serve_docs.py                    # Serve build/package on port 8000
    python3 serve_docs.py 8080               # Serve build/package on port 8080
    python3 serve_docs.py 8080 dist/package  # Serve dist/package on port 8080

The server will print the URL to share with students.
Press Ctrl+C to stop the server.
"""

import http.server
import socketserver
import sys
import os
import socket

def get_ip_address():
    """Get the local IP address for sharing with other computers"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS, doesn't actually send data
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    # Parse arguments
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    directory = sys.argv[2] if len(sys.argv) > 2 else "build/package"

    # Check if directory exists
    if not os.path.exists(directory):
        print(f"ERROR: Directory '{directory}' does not exist!")
        print(f"\nAvailable options:")
        if os.path.exists("build/package"):
            print("  - build/package (built package)")
        if os.path.exists("dist"):
            print("  - dist/* (distribution archives)")
        sys.exit(1)

    # Change to the directory
    os.chdir(directory)

    # Create server
    Handler = http.server.SimpleHTTPRequestHandler

    # Suppress default logging, we'll do our own
    class QuietHandler(Handler):
        def log_message(self, format, *args):
            # Only log errors
            if args[1][0] in ['4', '5']:  # HTTP error codes
                super().log_message(format, *args)

    try:
        httpd = socketserver.TCPServer(("", port), QuietHandler)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ ERROR: Port {port} is already in use!")
            print(f"\nOptions:")
            print(f"  1. Stop the existing server:")
            print(f"     pkill -f serve_docs.py")
            print(f"\n  2. Use a different port:")
            print(f"     make serve PORT=8080")
            print(f"\n  3. Find what's using the port:")
            print(f"     lsof -i :{port}")
            sys.exit(1)
        else:
            raise

    with httpd:
        ip = get_ip_address()

        print("=" * 70)
        print("📡 Documentation Server Started!")
        print("=" * 70)
        print(f"\nServing files from: {os.getcwd()}")
        print(f"\n🌐 Main URL (send this to students):")
        print(f"\n  ⭐ http://{ip}:{port}/")
        print(f"  ⭐ http://{ip}:{port}/index.html")
        print(f"\n📱 Local access (this computer):")
        print(f"    http://localhost:{port}/")
        print(f"\n📄 Individual pages:")
        print(f"    http://{ip}:{port}/QUICKSTART.html")
        print(f"    http://{ip}:{port}/README.html")
        print(f"    http://{ip}:{port}/INSTALL.html")
        print(f"    http://{ip}:{port}/INTERVIEW_PREP.html")
        print(f"    http://{ip}:{port}/Documentation/WATER_DATA.html")
        print(f"\n💡 Tip: Just send http://{ip}:{port}/ - students can navigate from there")
        print(f"\n⚠️  Press Ctrl+C to stop the server")
        print("=" * 70)
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    main()
