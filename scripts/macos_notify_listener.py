#!/usr/bin/env python3
"""
notify_listener.py

Simple local TCP listener that turns incoming lines into macOS notifications.
Python port of scripts/notify_listener.sh

Environment variables (all optional):
- BIND_IP: IP to bind (default: 127.0.0.1)
- TITLE: Notification title (default: AI Agent)
- NOTIFIER_CMD: Path to terminal-notifier binary
  (default: /Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier)
- SOUND: Sound name for terminal-notifier (default: default; empty to disable)

Usage:
  python3 scripts/notify_listener.py [PORT]
  ./scripts/notify_listener.py [PORT]

Input format (one JSON object per line):
  {
    "title": "Optional title, defaults to AI Agent",
    "message": "Required notification body",
    "status": "Optional status label, defaults to succeeded"
  }
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import socket
import subprocess
import sys

DEFAULT_PORT = 7777
DEFAULT_BIND_IP = os.environ.get("BIND_IP", "127.0.0.1")
DEFAULT_TITLE = os.environ.get("TITLE", "AI Agent")
DEFAULT_NOTIFIER_CMD = os.environ.get(
    "NOTIFIER_CMD",
    "/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier",
)


class Notifier:
    def __init__(self, title: str, notifier_cmd: str, sound: str | None):
        self.default_title = title
        self.sound = sound

        # Determine availability of terminal-notifier; respect explicit paths and PATH lookup
        cmd_path = None
        if notifier_cmd:
            if os.path.isabs(notifier_cmd) and os.path.exists(notifier_cmd):
                cmd_path = notifier_cmd
            else:
                cmd_path = shutil.which(notifier_cmd)

        if not cmd_path:
            resolved_cmd = notifier_cmd or "terminal-notifier"
            sys.stderr.write(
                f"terminal-notifier not found (looked for '{resolved_cmd}'). Install terminal-notifier and try again.\n"
            )
            sys.exit(1)

        self.terminal_notifier = cmd_path

    def _notify_terminal(self, *, title: str, message: str, status: str | None) -> None:
        args = [
            self.terminal_notifier,
            "-title",
            title,
            "-message",
            "✅" if status == "succeeded" else "⚠️" + " " + message,
            "-activate",
            "com.microsoft.VSCode",
        ]

        if status == "failed":
            self.sound = "basso"

        # if status:
        #     args.extend(["-subtitle", status])
        if self.sound:
            args.extend(["-sound", self.sound])
        try:
            subprocess.run(args, check=False)
        except Exception:
            # Swallow notification errors to keep listener alive
            pass

    def notify(
        self,
        *,
        message: str,
        title: str | None = None,
        status: str | None = None,
    ) -> None:
        resolved_title = title or self.default_title
        self._notify_terminal(title=resolved_title, message=message, status=status)


class Listener:
    def __init__(self, bind_ip: str, port: int, notifier: Notifier):
        self.bind_ip = bind_ip
        self.port = port
        self.notifier = notifier
        self._shutdown = False
        self._server_sock: socket.socket | None = None

    @staticmethod
    def _parse_payload(raw: str) -> tuple[str, str | None, str | None] | None:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            sys.stderr.write(f"Invalid JSON payload: {raw}\n")
            return None

        if not isinstance(payload, dict):
            sys.stderr.write("Payload must be a JSON object.\n")
            return None

        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            sys.stderr.write("Payload requires a non-empty 'message' field.\n")
            return None

        title = payload.get("title")
        if title is not None and not isinstance(title, str):
            sys.stderr.write("'title' must be a string when provided.\n")
            title = None

        status = payload.get("status")
        if status is None:
            status = "succeeded"
        elif not isinstance(status, str) or not status.strip():
            sys.stderr.write("'status' must be a non-empty string when provided.\n")
            status = "succeeded"

        return message, title, status

    def _handle_signals(self) -> None:
        def handler(signum, frame):
            # Print a newline for nicer Ctrl+C UX, match shell script behavior
            print("\nShutting down listener...")
            self._shutdown = True
            try:
                if self._server_sock:
                    self._server_sock.close()
            except Exception:
                pass

        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, handler)

    def serve_forever(self) -> None:
        self._handle_signals()

        print(f"Listening on {self.bind_ip}:{self.port} — title='{self.notifier.default_title}'  (Ctrl+C to stop)")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            self._server_sock = srv
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.bind_ip, self.port))
            srv.listen(5)
            while not self._shutdown:
                try:
                    conn, addr = srv.accept()
                except OSError:
                    # Likely closed during shutdown
                    break
                with conn:
                    try:
                        fileobj = conn.makefile("r", encoding="utf-8", errors="replace")
                    except Exception:
                        continue
                    for raw in fileobj:
                        line = raw.strip()
                        if not line:
                            continue
                        parsed = self._parse_payload(line)
                        if not parsed:
                            continue
                        message, title, status = parsed
                        self.notifier.notify(message=message, title=title, status=status)


def parse_port(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1]:
        try:
            p = int(argv[1])
            if p <= 0 or p > 65535:
                raise ValueError
            return p
        except ValueError:
            sys.stderr.write(f"Invalid port: {argv[1]}\n")
            sys.exit(2)
    return DEFAULT_PORT


def main() -> None:
    port = parse_port(sys.argv)
    notifier = Notifier(
        title=DEFAULT_TITLE,
        notifier_cmd=DEFAULT_NOTIFIER_CMD,
        sound="glass",
    )
    listener = Listener(
        bind_ip=DEFAULT_BIND_IP,
        port=port,
        notifier=notifier,
    )
    listener.serve_forever()


if __name__ == "__main__":
    main()
