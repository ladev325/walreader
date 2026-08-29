#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import threading
import time

COLOR_FILE = Path.home() / ".cache" / "wal" / "walreader.json"
PORT = 6767

data = None

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): return
    def do_GET(self):
        global data
        if data is None:
            self.send_response(503)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            print('[Wal Reader] 🕆 Sent: 503, data = None')
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(data.encode("utf-8"))
            print(f'[Wal Reader] Sent: \n{data}')

def check_file():
    global data
    while True:
        try:
            with open(COLOR_FILE, 'r', encoding='utf-8') as file:
                data = file.read()
        except FileNotFoundError:
            print('[Wal Reader] 🕆 Color file not found')
        time.sleep(1)

print(f'[Wal Reader] The server is running on http://localhost:{PORT}')
threading.Thread(target=check_file, daemon=True).start()
HTTPServer(("localhost", PORT), Handler).serve_forever()