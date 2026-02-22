import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

last_booking = {"seq": 0, "data": None}

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path.startswith("/last"):
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(last_booking).encode("utf-8"))
        else:
            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error":"not_found"}).encode("utf-8"))

    def do_POST(self):
        if self.path.startswith("/book"):
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except Exception:
                data = {}
            last_booking["seq"] += 1
            last_booking["data"] = data
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"ok": True, "seq": last_booking["seq"]}).encode("utf-8"))
        else:
            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error":"not_found"}).encode("utf-8"))

def run(host="127.0.0.1", port=5515):
    httpd = HTTPServer((host, port), Handler)
    print(f"Broker server running at http://{host}:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5515
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except Exception:
            pass
    run(host, port)
