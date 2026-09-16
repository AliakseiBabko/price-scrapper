"""Serve the repo over localhost and open the walkable view.

A browser will not fetch the .glb from a file:// page - the loader's request is
blocked as a cross-origin read, and the viewer sits on "loading..." with a
console error most people never open. So the viewer is served rather than
double-clicked.

    .venv\\Scripts\\python.exe tools\\blender\\serve_walk_viewer.py

Read-only: it serves the working tree and writes nothing.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import socket
import socketserver
import threading
import webbrowser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VIEWER = "tools/blender/walk_viewer.html"
DEFAULT_GLB = "data/outputs/variants/v0-existing/model.glb"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # noqa: A003 - stdlib signature
        pass

    def end_headers(self):
        # .glb is not in every stdlib mimetypes table; be explicit.
        if self.path.endswith(".glb"):
            self.send_header("Content-Type", "model/gltf-binary")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def free_port(preferred: int) -> int:
    with contextlib.closing(socket.socket()) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", default=DEFAULT_GLB, help="model to load, relative to the repo root")
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    glb = REPO / args.glb
    if not glb.is_file():
        print("No model at %s\nBuild one first:\n"
              "  tools\\blender\\bin\\blender-5.2.0-windows-x64\\blender.exe --background \\\n"
              "    --python tools\\blender\\export_glb.py -- <model.ifc> <model.glb> <report.json> <bonsai-site>"
              % glb)
        return 2

    port = free_port(args.port)
    rel = args.glb.replace("\\", "/")
    # The viewer resolves ?glb= against its own directory, so step back to the root.
    url = "http://127.0.0.1:%d/%s?glb=%s" % (port, VIEWER, "../../" + rel)

    handler = functools.partial(QuietHandler, directory=str(REPO))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print("serving %s\n  %s\n\nCtrl+C to stop." % (REPO, url))
        if not args.no_open:
            threading.Timer(0.4, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
