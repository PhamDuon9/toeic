"""
TOEIC Practice Test — Local Server
Usage: python serve.py
Then open: http://localhost:8000/app/
"""
import http.server, socketserver, os

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress request logs

print(f"TOEIC server running at http://localhost:{PORT}/app/")
print("Press Ctrl+C to stop.")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
