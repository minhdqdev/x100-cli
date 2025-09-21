#!/usr/bin/env python3
"""
notify_listener.py

Simple local TCP listener that turns incoming lines into macOS notifications.
Python port of scripts/notify_listener.sh

Environment variables (all optional):
- BIND_IP: IP to bind (default: 127.0.0.1)
- TITLE: Notification title (default: notify)
- LOG_FILE: Path to append logs (default: ~/.notify.log)
- NOTIFIER_CMD: Path to terminal-notifier binary
  (default: /Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier)
- SOUND: Sound name for terminal-notifier (default: default; empty to disable)

Usage:
  python3 scripts/notify_listener.py [PORT]
  ./scripts/notify_listener.py [PORT]
"""

from __future__ import annotations

import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_PORT = 7777
DEFAULT_BIND_IP = os.environ.get("BIND_IP", "127.0.0.1")
DEFAULT_TITLE = os.environ.get("TITLE", "AI Agent")
DEFAULT_LOG_FILE = os.environ.get("LOG_FILE", str(Path.home() / ".notify.log"))
DEFAULT_NOTIFIER_CMD = os.environ.get(
    "NOTIFIER_CMD",
    "/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier",
)
DEFAULT_SOUND = os.environ.get("SOUND", "glass")


class Notifier:
    def __init__(self, title: str, notifier_cmd: str, sound: str | None):
        self.title = title
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

    def _notify_terminal(self, message: str) -> None:
        args = [self.terminal_notifier, "-title", self.title, "-message", message, "-activate", "com.apple.Safari"]
        if self.sound:
            args.extend(["-sound", self.sound])
        try:
            subprocess.run(args, check=False)
        except Exception:
            # Swallow notification errors to keep listener alive
            pass

    def notify(self, message: str) -> None:
        self._notify_terminal(message)


class Listener:
    def __init__(self, bind_ip: str, port: int, log_file: str, notifier: Notifier):
        self.bind_ip = bind_ip
        self.port = port
        self.log_file = log_file
        self.notifier = notifier
        self._shutdown = False
        self._server_sock: socket.socket | None = None

    def _setup_logging(self) -> None:
        try:
            Path(self.log_file).touch(exist_ok=True)
        except Exception as e:
            sys.stderr.write(f"Cannot write to {self.log_file}: {e}\n")
            sys.exit(1)

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

    def _log(self, line: str) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{ts}  {line}\n")
        except Exception:
            # Non-fatal
            pass

    def serve_forever(self) -> None:
        self._setup_logging()
        self._handle_signals()

        print(f"Listening on {self.bind_ip}:{self.port} — title='{self.notifier.title}'  (Ctrl+C to stop)")
        print(f"Logging to: {self.log_file}")

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
                        line = raw.rstrip("\r\n")
                        if not line or not line.strip():
                            continue
                        self.notifier.notify(line)
                        self._log(line)


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
        sound=(DEFAULT_SOUND if DEFAULT_SOUND != "" else None),
    )
    listener = Listener(
        bind_ip=DEFAULT_BIND_IP,
        port=port,
        log_file=DEFAULT_LOG_FILE,
        notifier=notifier,
    )
    listener.serve_forever()


if __name__ == "__main__":
    main()
