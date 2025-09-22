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

Usage:
  python3 scripts/notify_listener.py [--speak] [PORT]
  ./scripts/notify_listener.py [--speak] [PORT]

Input format (one JSON object per line):
  {
    "title": "Optional title, defaults to AI Agent",
    "message": "Required notification body",
    "status": "Optional status label, defaults to succeeded"
  }
"""

from __future__ import annotations

import contextlib
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
    def __init__(self, title: str, notifier_cmd: str, speak: bool = False):
        self.default_title = title
        self.speak = speak

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
            ("✅" if status == "succeeded" else "⚠️") + " " + message,
            "-activate",
            "com.microsoft.VSCode",
        ]

        args.extend(["-sound", "glass" if status == "succeeded" else "basso"])

        try:
            subprocess.run(args, check=False)
        except Exception:
            # Swallow notification errors to keep listener alive
            pass

    def _speak(self, message: str) -> None:
        # Attempt to use macOS 'say' to speak the message; ignore failures
        say_cmd = shutil.which("say") or "/usr/bin/say"
        try:
            subprocess.run([say_cmd, message], check=False)
        except Exception:
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
        if self.speak:
            self._speak(message)


class Listener:
    def __init__(self, bind_ip: str, port: int, notifier: Notifier, close_after_message: bool = True):
        self.bind_ip = bind_ip
        self.port = port
        self.notifier = notifier
        self.close_after_message = close_after_message
        self._shutdown = False
        self._server_sock: socket.socket | None = None
        self._active_conn: socket.socket | None = None

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
            if self._server_sock:
                with contextlib.suppress(Exception):
                    self._server_sock.close()
                self._server_sock = None
            if self._active_conn:
                with contextlib.suppress(Exception):
                    self._active_conn.shutdown(socket.SHUT_RDWR)
                with contextlib.suppress(Exception):
                    self._active_conn.close()
                self._active_conn = None

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
            srv.settimeout(1.0)
            while not self._shutdown:
                try:
                    conn, addr = srv.accept()
                except socket.timeout:
                    continue
                except OSError:
                    # Likely closed during shutdown
                    if self._shutdown:
                        break
                    break
                with conn:
                    self._active_conn = conn
                    try:
                        fileobj = conn.makefile("r", encoding="utf-8", errors="replace")
                    except Exception:
                        self._active_conn = None
                        continue
                    try:
                        while not self._shutdown:
                            raw = fileobj.readline()
                            if not raw:
                                break
                            line = raw.strip()
                            if not line:
                                continue
                            parsed = self._parse_payload(line)
                            if not parsed:
                                continue
                            message, title, status = parsed
                            self.notifier.notify(message=message, title=title, status=status)
                            # Close connection after handling one message so clients like `nc` exit.
                            if self.close_after_message:
                                break
                    finally:
                        with contextlib.suppress(Exception):
                            fileobj.close()
                        self._active_conn = None
            self._server_sock = None


def parse_args(argv: list[str]) -> tuple[int, bool]:
    """Parse command-line args: [--speak] [PORT].

    Returns (port, speak)
    """
    speak = False
    port: int | None = None
    remaining: list[str] = []

    for a in argv[1:]:
        if a == "--speak":
            speak = True
        elif a.startswith("-"):
            sys.stderr.write(f"Unknown option: {a}\n")
            sys.exit(2)
        else:
            remaining.append(a)

    if remaining:
        candidate = remaining[0]
        try:
            p = int(candidate)
            if p <= 0 or p > 65535:
                raise ValueError
            port = p
        except ValueError:
            sys.stderr.write(f"Invalid port: {candidate}\n")
            sys.exit(2)

    if port is None:
        port = DEFAULT_PORT

    return port, speak


def main() -> None:
    port, speak = parse_args(sys.argv)
    notifier = Notifier(
        title=DEFAULT_TITLE,
        notifier_cmd=DEFAULT_NOTIFIER_CMD,
        speak=speak,
    )
    listener = Listener(
        bind_ip=DEFAULT_BIND_IP,
        port=port,
        notifier=notifier,
        close_after_message=(os.environ.get("CLOSE_AFTER_MESSAGE", "1").lower() not in {"0", "false", "no"}),
    )
    listener.serve_forever()


if __name__ == "__main__":
    main()
