"""CLI entrypoint for the x100 tool."""
from __future__ import annotations

import argparse
from typing import Sequence

from . import ui
from .core import (
    detect_tool_paths,
    disable_agent,
    disable_command,
    enable_agent,
    enable_command,
    enable_workflow,
    init_project,
    list_available_agents,
    list_available_commands,
    manage_agents,
    manage_commands,
    run_contribute,
    run_menu,
    verify,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="x100", description="x100 project automation CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", aliases=["initialize", "init-project"], help="Initialize project structure")
    sub.add_parser("contribute", help="Sync and open a PR with changes")
    sub.add_parser("verify", help="Run environment checks")

    cmd_parser = sub.add_parser("command", help="Manage Claude Code commands")
    cmd_sub = cmd_parser.add_subparsers(dest="subcommand")
    cmd_sub.add_parser("list", help="List all available commands")
    enable_cmd = cmd_sub.add_parser("enable", help="Enable a command")
    enable_cmd.add_argument("name", nargs="?", help="Command name to enable")
    disable_cmd = cmd_sub.add_parser("disable", help="Disable a command")
    disable_cmd.add_argument("name", nargs="?", help="Command name to disable")

    agent_parser = sub.add_parser("agent", help="Manage Claude Code agents")
    agent_sub = agent_parser.add_subparsers(dest="subcommand")
    agent_sub.add_parser("list", help="List all available agents")
    enable_agent_cmd = agent_sub.add_parser("enable", help="Enable an agent")
    enable_agent_cmd.add_argument("name", nargs="?", help="Agent name to enable")
    disable_agent_cmd = agent_sub.add_parser("disable", help="Disable an agent")
    disable_agent_cmd.add_argument("name", nargs="?", help="Agent name to disable")

    sub.add_parser("workflow-enable", help="Enable all workflow commands and agents")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = detect_tool_paths()

    command = args.command

    if command in ("init", "initialize", "init-project"):
        ui.clear_screen()
        init_project(paths, wait_for_key=False)
        return
    if command == "contribute":
        ui.clear_screen()
        run_contribute(paths)
        return
    if command == "verify":
        ui.clear_screen()
        verify(paths)
        return
    if command == "workflow-enable":
        ui.clear_screen()
        enable_workflow(paths)
        return

    if command == "command":
        ui.clear_screen()
        subcommand = getattr(args, "subcommand", None)
        if subcommand == "list":
            list_available_commands(paths)
        elif subcommand == "enable":
            enable_command(paths, getattr(args, "name", None))
        elif subcommand == "disable":
            disable_command(paths, getattr(args, "name", None))
        else:
            manage_commands(paths)
        return

    if command == "agent":
        ui.clear_screen()
        subcommand = getattr(args, "subcommand", None)
        if subcommand == "list":
            list_available_agents(paths)
        elif subcommand == "enable":
            enable_agent(paths, getattr(args, "name", None))
        elif subcommand == "disable":
            disable_agent(paths, getattr(args, "name", None))
        else:
            manage_agents(paths)
        return

    ui.clear_screen()
    run_menu(paths)


if __name__ == "__main__":  # pragma: no cover
    main()
