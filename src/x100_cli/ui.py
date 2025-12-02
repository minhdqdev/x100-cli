"""Terminal UI helpers for the x100 CLI."""

from __future__ import annotations

import os
import sys
import shutil
from typing import Callable, Sequence
from rich.tree import Tree
from pathlib import Path
from rich.text import Text
from rich.align import Align
from rich.tree import Tree
from rich.console import Console

console = Console()

BANNER = """
/====================================================\\
||     █████ █████ ████     █████       █████       ||
||    ░░███ ░░███ ░░███   ███░░░███   ███░░░███     ||
||     ░░███ ███   ░███  ███   ░░███ ███   ░░███    ||
||      ░░█████    ░███ ░███    ░███░███    ░███    ||
||       ███░███   ░███ ░███    ░███░███    ░███    ||
||      ███ ░░███  ░███ ░░███   ███ ░░███   ███     ||
||     █████ █████ █████ ░░░█████░   ░░░█████░      ||
||    ░░░░░ ░░░░░ ░░░░░    ░░░░░░      ░░░░░░       ||
\\====================================================/"""

TAGLINE = "x100 - Create high-grade software at speed with AI agents"

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
REVERSE = "\x1b[7m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"


class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """

    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {
            "pending": 0,
            "running": 1,
            "done": 2,
            "error": 3,
            "skipped": 4,
        }
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append(
                {"key": key, "label": label, "status": "pending", "detail": ""}
            )
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append(
            {"key": key, "label": key, "status": status, "detail": detail}
        )
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = (
                        f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                    )
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


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
    print(BANNER)
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
    print(BANNER)
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


def interactive_select(
    title: str, options: Sequence[str], default_index: int = 0
) -> int | None:
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


def prompt_choice(
    question: str, options: Sequence[str], default_index: int | None = None
) -> int:
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


CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"


def check_file(key: str, file_path: Path, tracker: StepTracker = None) -> bool:
    """Check if a file exists. Optionally update tracker.

    Args:
        file_path: Path to the file to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if file exists, False otherwise
    """
    exists = file_path.is_file()
    if tracker:
        if exists:
            tracker.complete(key, "found")
        else:
            tracker.error(key, "not found")
    return exists


def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/github/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True

    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found


def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split("\n")
    colors = [
        "orange_red1",
        "dark_orange",
        "orange1",
        "orange1",
        "wheat1",
        "light_goldenrod1",
    ]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic orange_red1")))
    console.print()
