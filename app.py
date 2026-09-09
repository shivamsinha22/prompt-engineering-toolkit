import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from toolkit.prompt_builder import PromptBuilder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "strategies.json")
HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
builder = PromptBuilder(TEMPLATE_PATH)


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, content_type, body):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            with open(HTML_PATH, "rb") as f:
                self._send(200, "text/html; charset=utf-8", f.read())
            return

        if path == "/strategies":
            self._send(200, "application/json; charset=utf-8",
                       json.dumps(builder.list_strategies()))
            return

        self._send(404, "application/json; charset=utf-8",
                   json.dumps({"error": "Not found"}))

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/generate":
            self._send(404, "application/json; charset=utf-8",
                       json.dumps({"error": "Not found"}))
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))

            strategy = payload.get("strategy", "").strip()
            variables = payload.get("variables", {})

            if not strategy:
                raise ValueError("Please select a strategy.")
            if not isinstance(variables, dict):
                raise ValueError("Variables must be an object.")

            prompt = builder.build(strategy, variables)
            response = {"success": True, "strategy": strategy, "prompt": prompt}
            self._send(200, "application/json; charset=utf-8",
                       json.dumps(response))
        except Exception as exc:
            self._send(400, "application/json; charset=utf-8",
                       json.dumps({"success": False, "error": str(exc)}))

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Prompt Engineering Toolkit running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
