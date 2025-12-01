"""Terminal UI helpers for the x100 CLI."""
from __future__ import annotations

import os
import sys
from typing import Callable, Sequence

TITLE = """
/====================================================\\
||                                                  ||
||     █████ █████ ████     █████       █████       ||
||    ░░███ ░░███ ░░███   ███░░░███   ███░░░███     ||
||     ░░███ ███   ░███  ███   ░░███ ███   ░░███    ||
||      ░░█████    ░███ ░███    ░███░███    ░███    ||
||       ███░███   ░███ ░███    ░███░███    ░███    ||
||      ███ ░░███  ░███ ░░███   ███ ░░███   ███     ||
||     █████ █████ █████ ░░░█████░   ░░░█████░      ||
||    ░░░░░ ░░░░░ ░░░░░    ░░░░░░      ░░░░░░       ||
||                                                  ||
\\====================================================/"""

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
REVERSE = "\x1b[7m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"


if os.name == "nt":  # pragma: no cover - interactive Windows behavior
    import msvcrt  # type: ignore

    def read_key() -> str:
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            mapping = {b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT"}
            return mapping.get(ch2, "")
        if ch == b"\r":
            return "ENTER"
        if ch == b"\x1b":
            return "ESC"
        return ch.decode(errors="ignore")

else:  # pragma: no cover - requires interactive terminal
    import termios
    import tty

    def read_key() -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    return "UP"
                if seq == "[B":
                    return "DOWN"
                if seq == "[C":
                    return "RIGHT"
                if seq == "[D":
                    return "LEFT"
                return "ESC"
            if ch in ("\r", "\n"):
                return "ENTER"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen() -> None:
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            sys.stdout.write("\x1b[2J\x1b[3J\x1b[H")
            sys.stdout.flush()
    except Exception:
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            sys.stdout.write("\n" * 100)
            sys.stdout.flush()


def prompt_yes_no(question: str, default: bool = False) -> bool:
    hint = "Y/n" if default else "y/N"
    sys.stdout.write(f"{question} [{hint}]: ")
    sys.stdout.flush()
    try:
        choice = input("").strip().lower()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return False
    if not choice:
        return default
    return choice in ("y", "yes")


def prompt_text(
    question: str,
    default: str = "",
    validator: Callable[[str], bool] | None = None,
) -> str:
    while True:
        hint = f" [{default}]" if default else ""
        sys.stdout.write(f"{question}{hint}: ")
        sys.stdout.flush()
        try:
            val = input("")
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            return default
        val = val.strip() or default
        if validator is None or validator(val):
            return val
        print(f"{YELLOW}Invalid value. Please try again.{RESET}")


def render_menu(items: Sequence[str], selected: int) -> None:
    clear_screen()
    print(TITLE)
    print()
    print(f"{BOLD}Use ↑/↓ to navigate, Enter or number to select.{RESET}")
    print()
    for idx, label in enumerate(items):
        prefix = f" {idx + 1}. "
        if idx == selected:
            print(f"{REVERSE}{prefix}{label}{RESET}")
        else:
            print(f"{prefix}{label}")
    print()
    print(f"{DIM}Press ESC or Ctrl+C to exit.{RESET}")


def render_submenu(title: str, items: Sequence[str], selected: int) -> None:
    clear_screen()
    print(TITLE)
    print()
    print(f"{BOLD}{title}{RESET}")
    print(f"{DIM}Use ↑/↓ to navigate, Enter or number to select. ESC to cancel.{RESET}")
    print()
    for idx, label in enumerate(items):
        prefix = f" {idx + 1}. "
        if idx == selected:
            print(f"{REVERSE}{prefix}{label}{RESET}")
        else:
            print(f"{prefix}{label}")


def interactive_select(title: str, options: Sequence[str], default_index: int = 0) -> int | None:
    if not options:
        return None
    selected = max(0, min(default_index, len(options) - 1))
    while True:
        render_submenu(title, options, selected)
        try:
            key = read_key()
        except KeyboardInterrupt:
            return None
        if key == "UP":
            selected = (selected - 1) % len(options)
        elif key == "DOWN":
            selected = (selected + 1) % len(options)
        elif key == "ENTER":
            return selected
        elif key in ("ESC", "q"):
            return None
        elif key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(options):
                return idx


def prompt_choice(question: str, options: Sequence[str], default_index: int | None = None) -> int:
    idx = interactive_select(question, options, default_index or 0)
    if idx is None:
        return default_index or 0
    return idx


def pause(message: str = "Press Enter to return to menu…") -> None:
    input(message)


def menu_loop(options: Sequence[str], actions: Sequence[Callable[[], None]]) -> None:
    if len(options) != len(actions):
        raise ValueError("Options and actions must have the same length")
    selected = 0
    while True:
        try:
            render_menu(options, selected)
            key = read_key()
            if key == "UP":
                selected = (selected - 1) % len(options)
            elif key == "DOWN":
                selected = (selected + 1) % len(options)
            elif key.isdigit():
                idx = int(key) - 1
                if 0 <= idx < len(options):
                    clear_screen()
                    actions[idx]()
            elif key == "ENTER":
                clear_screen()
                actions[selected]()
            elif key in ("ESC", "q"):
                clear_screen()
                sys.exit(0)
        except KeyboardInterrupt:
            clear_screen()
            sys.exit(0)
