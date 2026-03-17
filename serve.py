#!/usr/bin/env python3
"""
hackathon-server — serves ~/hackathon/ for Playwright and local access
http://0.0.0.0:8767
"""
import http.server, socket, os, sys

PORT      = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
DIRECTORY = os.path.expanduser("~/hackathon")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise

if __name__ == "__main__":
    ip = get_local_ip()
    url_local   = f"http://localhost:{PORT}/"
    url_network = f"http://{ip}:{PORT}/"

    print(f"\n  Hackathon Server")
    print(f"  Local:   {url_local}")
    print(f"  Network: {url_network}")
    print(f"\n  Ctrl+C to stop\n")

    with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
