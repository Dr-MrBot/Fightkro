import http.server
import socketserver
import mimetypes
import webbrowser
import os
import sys
import urllib.request
import base64

# Ensure working directory is the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Register custom MIME types for 3D models and game assets
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/woff', '.woff')

SIGNAL_GATEWAY = base64.b64decode(b'aHR0cHM6Ly9maWdodGthcm8uY29t').decode('utf-8')

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/room'):
            self.handle_proxy()
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/room'):
            self.handle_proxy()
            return
        super().do_POST()

    def handle_proxy(self):
        target_url = SIGNAL_GATEWAY + self.path
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            req = urllib.request.Request(target_url, data=body, method=self.command)
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'content-length']:
                    req.add_header(header, value)

            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"error":"Signaling unavailable"}')

    def log_message(self, format, *args):
        sys.stdout.write(f"\r[FightKro] Serving: {args[0]}                    ")
        sys.stdout.flush()

PORT = 8080
for p in range(8080, 8095):
    try:
        httpd = socketserver.TCPServer(('127.0.0.1', p), GameHTTPRequestHandler)
        PORT = p
        break
    except OSError:
        continue

url = f"http://localhost:{PORT}/"
print("\n" + "="*58)
print("             FIGHTKRO - SANSAD SHOWDOWN")
print("          Creator & Developer: Dr-MrBot")
print(f"      Game running locally at: {url}")
print("="*58)
print("\nOpening your default browser...")
print("Press Ctrl+C in this window to stop the server anytime.\n")

webbrowser.open(url)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nGame server stopped.")
    sys.exit(0)
