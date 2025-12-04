"""Core operations for the x100 CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from . import ui


X100_CONFIG_PATH = Path.cwd() / ".x100" / "config.json"


def load_config() -> None:
    """Load configuration from .x100/config.json in the current working directory."""

    if not X100_CONFIG_PATH.exists():
        return {}

    try:
        cfg_text = X100_CONFIG_PATH.read_text(encoding="utf-8")
        cfg_data = json.loads(cfg_text)
        if isinstance(cfg_data, dict):
            return cfg_data
    except Exception:
        return {}


X100_CONFIG = load_config()


def save_config(config: dict, config_path: Path = None) -> None:
    """Save configuration to .x100/config.json."""
    if config_path is None:
        config_path = X100_CONFIG_PATH
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


@dataclass(frozen=True)
class ToolPaths:
    """Locations the CLI depends on."""

    tool_root: Path
    outer_dir: Path

    @property
    def resources_dir(self) -> Path:
        return self.tool_root / "resources"

    @property
    def claude_dir(self) -> Path:
        return self.outer_dir / ".claude"


def detect_tool_paths() -> ToolPaths:
    current = Path(__file__).resolve()
    tool_root = _locate_tool_root(current)
    return ToolPaths(tool_root=tool_root, outer_dir=tool_root.parent)


def _locate_tool_root(start: Path) -> Path:
    for candidate in start.parents:
        if (candidate / "resources").is_dir():
            return candidate
    # Fallback to src/..
    return start.parents[2]


def setup_vscode(paths: ToolPaths) -> None:
    src = paths.resources_dir / "vscode" / "settings.example.json"
    target_dir = paths.outer_dir / ".vscode"
    target = target_dir / "settings.json"

    if not src.exists():
        print(f"{ui.RED}Source not found:{ui.RESET} {src}")
        ui.pause()
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        src_cfg = json.loads(src.read_text(encoding="utf-8"))
        if not isinstance(src_cfg, dict):
            raise ValueError("Source settings must be a JSON object")
    except Exception as exc:  # pragma: no cover - defensive
        print(f"{ui.RED}Error reading source settings:{ui.RESET} {exc}")
        ui.pause()
        return

    if not target.exists():
        target.write_text(
            json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"{ui.GREEN}CREATED{ui.RESET} {target}")
        ui.pause()
        return

    try:
        dst_cfg = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(dst_cfg, dict):
            raise ValueError("Target settings must be a JSON object")
    except Exception as exc:
        print(f"{ui.YELLOW}Warning:{ui.RESET} cannot parse existing settings: {exc}")
        if ui.prompt_yes_no("Replace with example settings?", default=False):
            target.write_text(
                json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"{ui.GREEN}UPDATED{ui.RESET} {target} (replaced)")
        else:
            print(f"{ui.YELLOW}Skipped.{ui.RESET} Existing settings preserved.")
        ui.pause()
        return

    merged = dict(dst_cfg)
    changes = 0
    for key, src_val in src_cfg.items():
        if key not in dst_cfg:
            merged[key] = src_val
            print(f"{ui.GREEN}ADD{ui.RESET} {key}")
            changes += 1
        elif dst_cfg[key] != src_val:
            print()
            print(f"{ui.YELLOW}Conflict for key:{ui.RESET} {ui.BOLD}{key}{ui.RESET}")
            print(f"  Existing: {dst_cfg[key]}")
            print(f"  Example:  {src_val}")
            if ui.prompt_yes_no("Overwrite with example value?", default=False):
                merged[key] = src_val
                print(f"{ui.GREEN}SET{ui.RESET} {key} -> example value")
                changes += 1
            else:
                print(f"{ui.YELLOW}KEEP{ui.RESET} {key} -> existing value")

    if changes:
        target.write_text(
            json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"\n{ui.GREEN}UPDATED{ui.RESET} {target} ({changes} changes)")
    else:
        print(f"{ui.GREEN}No changes needed.{ui.RESET} {target} already up to date")

    ui.pause()


def setup_ai_agent(paths: ToolPaths) -> None:
    choices = ["Claude Code", "Gemini CLI", "OpenAI Codex", "Exit"]
    idx = ui.interactive_select(
        "Setup AI Agent - Choose an option", choices, default_index=0
    )
    if idx is None or choices[idx] == "Exit":
        return
    if choices[idx] == "Claude Code":
        setup_claude_code(paths)
    elif choices[idx] == "Gemini CLI":
        overwrite_agents_md(paths, "Gemini CLI")
    elif choices[idx] == "OpenAI Codex":
        overwrite_agents_md(paths, "OpenAI Codex")
    else:  # pragma: no cover - defensive
        print(f"{ui.YELLOW}Not implemented yet:{ui.RESET} {choices[idx]}")
        ui.pause()


def setup_claude_code(paths: ToolPaths) -> None:
    src_root = paths.resources_dir / "claude"
    dst_root = paths.claude_dir

    print(f"This will copy and overwrite contents in: {dst_root}")
    if not ui.prompt_yes_no("Proceed?", default=False):
        print(f"{ui.YELLOW}Cancelled by user.{ui.RESET}")
        ui.pause()
        return

    dst_root.mkdir(parents=True, exist_ok=True)

    dir_items = ["agents", "commands"]
    file_items = ["settings.json", "statusline.sh"]

    for dname in dir_items:
        src_dir = src_root / dname
        dst_dir = dst_root / dname
        if dst_dir.exists():
            shutil.rmtree(dst_dir, ignore_errors=True)
        if src_dir.is_dir():
            shutil.copytree(src_dir, dst_dir)
            print(f"{ui.GREEN}COPIED{ui.RESET} {dname}/")
        else:
            print(
                f"{ui.YELLOW}SKIP{ui.RESET} Missing directory in resources: {src_dir}"
            )

    for fname in file_items:
        src_file = src_root / fname
        dst_file = dst_root / fname
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            if dst_file.suffix == ".sh":
                try:
                    dst_file.chmod(dst_file.stat().st_mode | 0o111)
                except Exception:  # pragma: no cover - permissions
                    pass
            print(f"{ui.GREEN}COPIED{ui.RESET} {fname}")
        else:
            print(f"{ui.YELLOW}SKIP{ui.RESET} Missing file in resources: {src_file}")

    print(f"\n{ui.GREEN}Claude Code assets installed to{ui.RESET} {dst_root}")
    ui.pause()


def overwrite_agents_md(paths: ToolPaths, provider: str) -> None:
    src = paths.resources_dir / "AGENTS.example.md"
    dst = paths.outer_dir / "AGENTS.md"
    if not src.exists():
        print(f"{ui.RED}Missing resource:{ui.RESET} {src}")
        ui.pause()
        return
    try:
        shutil.copyfile(src, dst)
        print(
            f"{ui.GREEN}OVERWROTE{ui.RESET} AGENTS.md using template for {provider}: {dst}"
        )
    except Exception as exc:  # pragma: no cover - filesystem errors
        print(f"{ui.RED}ERROR{ui.RESET} Overwriting AGENTS.md failed: {exc}")
    ui.pause()


def verify(paths: ToolPaths) -> None:
    tool_dir = paths.tool_root
    outer_dir = paths.outer_dir

    print(f"{ui.BOLD}Verification Results{ui.RESET}\n")

    all_ok = True

    if tool_dir.name == ".x100":
        print(
            f"{ui.GREEN}OK{ui.RESET}    Current directory name is '.x100' -> {tool_dir}"
        )
    else:
        all_ok = False
        print(
            f"{ui.RED}FAIL{ui.RESET}  Expected parent tool directory to be named '.x100' but got '"
            f"{tool_dir.name}' at {tool_dir}"
        )

    dotgit = outer_dir / ".git"
    if dotgit.is_dir() or dotgit.is_file():
        print(
            f"{ui.GREEN}OK{ui.RESET}    Outer directory appears to be a git repo -> {outer_dir}"
        )
    else:
        all_ok = False
        print(
            f"{ui.RED}FAIL{ui.RESET}  Outer directory is not a git repo -> {outer_dir}"
        )

    required_items = [
        ("dir", "src"),
        ("dir", "docs"),
        ("file", "README.md"),
        ("file", "AGENTS.md"),
    ]

    for kind, name in required_items:
        path = outer_dir / name
        exists = path.is_dir() if kind == "dir" else path.is_file()
        if exists:
            print(f"{ui.GREEN}OK{ui.RESET}    {name} -> {path}")
        else:
            all_ok = False
            print(f"{ui.RED}MISS{ui.RESET}  {name} (expected at {path})")

    print()
    if all_ok:
        print(f"{ui.GREEN}All checks passed.{ui.RESET}")
    else:
        print(
            f"{ui.YELLOW}Some checks failed. Please review the output above.{ui.RESET}"
        )
    ui.pause()


def init_project(paths: ToolPaths, wait_for_key: bool = True) -> None:
    tool_dir = paths.tool_root
    outer_dir = paths.outer_dir
    resources_dir = paths.resources_dir

    print(f"{ui.BOLD}Initializing Project Structure{ui.RESET}\n")

    for dname in ["src", "docs", "tests", "scripts"]:
        path = outer_dir / dname
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
            print(f"{ui.GREEN}CREATED{ui.RESET} {path}")
        else:
            print(f"{ui.GREEN}OK{ui.RESET}      {path}")

    src_readme = resources_dir / "README.example.md"
    dst_readme = outer_dir / "README.md"
    if not dst_readme.exists():
        if src_readme.exists():
            shutil.copyfile(src_readme, dst_readme)
            print(f"{ui.GREEN}CREATED{ui.RESET} {dst_readme} from resources")
        else:
            print(f"{ui.RED}MISSING{ui.RESET} Resource not found: {src_readme}")
    else:
        print(f"{ui.GREEN}OK{ui.RESET}      README.md already exists -> {dst_readme}")

    src_agents = resources_dir / "AGENTS.example.md"
    dst_agents = outer_dir / "AGENTS.md"
    if not dst_agents.exists():
        if src_agents.exists():
            shutil.copyfile(src_agents, dst_agents)
            print(f"{ui.GREEN}CREATED{ui.RESET} {dst_agents} from resources")
        else:
            print(f"{ui.RED}MISSING{ui.RESET} Resource not found: {src_agents}")
    else:
        print(f"{ui.GREEN}OK{ui.RESET}      AGENTS.md already exists -> {dst_agents}")

    dotgit = outer_dir / ".git"
    if dotgit.exists():
        print(f"{ui.GREEN}OK{ui.RESET}      Git repo detected -> {outer_dir}")
    else:
        print(f"{ui.YELLOW}NO GIT{ui.RESET}  {outer_dir} is not a git repo.")
        if ui.prompt_yes_no("Initialize git repository here?", default=True):
            try:
                result = subprocess.run(
                    ["git", "init", str(outer_dir)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    print(
                        f"{ui.GREEN}INIT{ui.RESET}     Git repository initialized in {outer_dir}"
                    )
                else:
                    print(
                        f"{ui.RED}ERROR{ui.RESET}    git init failed: {result.stderr.strip()}"
                    )
            except FileNotFoundError:
                print(f"{ui.RED}ERROR{ui.RESET}    'git' command not found on PATH.")

    print()
    print(f"{ui.BOLD}Project Metadata{ui.RESET}")
    cfg_path = tool_dir / "config.json"
    config: dict[str, object] = {}
    if cfg_path.exists():
        try:
            existing = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                config.update(existing)
        except Exception as exc:
            print(
                f"{ui.YELLOW}Warning:{ui.RESET} could not read existing config: {exc}"
            )

    if not config.get("project_name"):
        name_default = outer_dir.name
        config["project_name"] = ui.prompt_text("Project name", default=name_default)

    if not config.get("project_code"):

        def _code_validator(value: str) -> bool:
            return len(value) > 0 and all(c.isalnum() or c in ("-", "_") for c in value)

        base = str(config.get("project_name", outer_dir.name))
        code_default = base.lower().replace(" ", "-")
        config["project_code"] = ui.prompt_text(
            "Project code (slug; letters, digits, - or _)",
            default=code_default,
            validator=_code_validator,
        )

    if "backend" not in config:
        backend_opts = ["None", "Python - no framework", "Python - Django"]
        be_idx = ui.prompt_choice(
            "Backend language/framework:", backend_opts, default_index=0
        )
        config["backend"] = [None, "python", "django"][be_idx]

    if "frontend" not in config:
        frontend_opts = ["None", "NodeJS - NextJS"]
        fe_idx = ui.prompt_choice(
            "Frontend language/framework:", frontend_opts, default_index=0
        )
        config["frontend"] = [None, "nextjs"][fe_idx]

    try:
        cfg_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"{ui.GREEN}SAVED{ui.RESET} Configuration -> {cfg_path}")
    except Exception as exc:
        print(f"{ui.RED}ERROR{ui.RESET} Saving config failed: {exc}")

    print()
    print(f"{ui.BOLD}Linking CLI{ui.RESET}")
    cli_src = tool_dir / "x100"
    link_path = outer_dir / "x100"

    def create_wrapper_script(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except Exception:
            pass

    try:
        need_link = True
        if link_path.is_symlink():
            if link_path.resolve() == cli_src.resolve():
                print(
                    f"{ui.GREEN}OK{ui.RESET}      Symlink already exists -> {link_path}"
                )
                need_link = False
            else:
                if ui.prompt_yes_no(
                    "A different symlink named 'x100' exists. Replace?", default=False
                ):
                    link_path.unlink()
                else:
                    need_link = False
        elif link_path.exists():
            if ui.prompt_yes_no(
                "An 'x100' file exists. Replace with symlink?", default=False
            ):
                link_path.unlink()
            else:
                need_link = False

        if need_link:
            try:
                link_path.symlink_to(cli_src)
                print(f"{ui.GREEN}LINKED{ui.RESET}   {link_path} -> {cli_src}")
            except (OSError, NotImplementedError):
                wrapper = """#!/usr/bin/env bash
exec \"$(dirname \"$0\")/.x100/x100\" \"$@\"
"""
                create_wrapper_script(link_path, wrapper)
                print(
                    f"{ui.YELLOW}WRAPPED{ui.RESET}  Created shell wrapper at {link_path}"
                )
    except Exception as exc:
        print(f"{ui.YELLOW}Note:{ui.RESET} Could not create POSIX launcher: {exc}")

    if sys.platform.startswith("win"):
        cmd_path = outer_dir / "x100.cmd"
        if not cmd_path.exists():
            try:
                cmd_content = '@echo off\r\n"%~dp0\\.x100\\x100.cmd" %*\r\n'
                create_wrapper_script(cmd_path, cmd_content)
                print(f"{ui.GREEN}CREATED{ui.RESET}  {cmd_path}")
            except Exception as exc:
                print(
                    f"{ui.YELLOW}Note:{ui.RESET} Could not create Windows launcher: {exc}"
                )

    if wait_for_key:
        ui.pause()


def run_contribute(paths: ToolPaths) -> None:
    script_path = paths.tool_root / "scripts" / "contribute.sh"
    if not script_path.exists():
        print(f"{ui.RED}ERROR{ui.RESET} contribute script not found: {script_path}")
        sys.exit(1)
    try:
        result = subprocess.run(["bash", str(script_path)])
        if result.returncode != 0:
            sys.exit(result.returncode)
    except FileNotFoundError:
        print(
            f"{ui.RED}ERROR{ui.RESET} 'bash' not found on PATH. Install bash to run contribute."
        )
        sys.exit(127)


def _list_markdown(dir_path: Path) -> list[str]:
    if not dir_path.exists():
        return []
    return sorted([f.name for f in dir_path.iterdir() if f.suffix == ".md"])


def list_available_commands(paths: ToolPaths) -> None:
    available_dir = paths.resources_dir / "claude" / "available-commands"
    active_dir = paths.claude_dir / "commands"

    print(f"{ui.BOLD}Available Commands{ui.RESET}\n")

    if not available_dir.exists():
        print(
            f"{ui.RED}ERROR{ui.RESET} Available commands directory not found: {available_dir}"
        )
        ui.pause("Press Enter to continue…")
        return

    available_files = _list_markdown(available_dir)
    active_files = _list_markdown(active_dir)

    for filename in available_files:
        name = filename[:-3]
        status = (
            f"{ui.GREEN}[ACTIVE]{ui.RESET}"
            if filename in active_files
            else f"{ui.DIM}[available]{ui.RESET}"
        )
        description = ""
        filepath = available_dir / filename
        try:
            lines = filepath.read_text(encoding="utf-8").splitlines()
            if len(lines) > 1 and lines[0].strip() == "---":
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if line.startswith("description:"):
                        description = line.split(":", 1)[1].strip()
                        break
        except Exception:
            pass

        print(f"  {status} /{name}")
        if description:
            print(f"      {ui.DIM}{description}{ui.RESET}")

    print()
    ui.pause("Press Enter to return to menu…")


def list_available_agents(paths: ToolPaths) -> None:
    available_dir = paths.resources_dir / "claude" / "available-agents"
    active_dir = paths.claude_dir / "agents"

    print(f"{ui.BOLD}Available Agents{ui.RESET}\n")

    if not available_dir.exists():
        print(
            f"{ui.RED}ERROR{ui.RESET} Available agents directory not found: {available_dir}"
        )
        ui.pause("Press Enter to continue…")
        return

    available_files = _list_markdown(available_dir)
    active_files = _list_markdown(active_dir)

    for filename in available_files:
        name = filename[:-3]
        status = (
            f"{ui.GREEN}[ACTIVE]{ui.RESET}"
            if filename in active_files
            else f"{ui.DIM}[available]{ui.RESET}"
        )
        description = ""
        filepath = available_dir / filename
        try:
            content = filepath.read_text(encoding="utf-8")
            if content.startswith("---"):
                end_idx = content.find("---", 3)
                if end_idx > 0:
                    frontmatter = content[3:end_idx]
                    for line in frontmatter.split("\n"):
                        if line.startswith("name:"):
                            name = line.split(":", 1)[1].strip()
                        elif line.startswith("description:"):
                            desc_line = line.split(":", 1)[1].strip()
                            description = (
                                desc_line[:80] + "..."
                                if len(desc_line) > 80
                                else (
                                    desc_line.split(".")[0] + "."
                                    if "." in desc_line
                                    else desc_line
                                )
                            )
        except Exception:
            pass

        print(f"  {status} {name}")
        if description:
            print(f"      {ui.DIM}{description}{ui.RESET}")

    print()
    ui.pause("Press Enter to return to menu…")


def _select_markdown(paths: ToolPaths, dir_path: Path, prompt: str) -> str | None:
    files = [f[:-3] for f in _list_markdown(dir_path)]
    if not files:
        return None
    idx = ui.interactive_select(prompt, files, default_index=0)
    if idx is None:
        return None
    return files[idx]


def enable_command(paths: ToolPaths, command_name: str | None = None) -> None:
    available_dir = paths.resources_dir / "claude" / "available-commands"
    active_dir = paths.claude_dir / "commands"
    active_dir.mkdir(parents=True, exist_ok=True)

    if not command_name:
        command_name = _select_markdown(
            paths, available_dir, "Select command to enable:"
        )
    if not command_name:
        return

    src = available_dir / f"{command_name}.md"
    dst = active_dir / f"{command_name}.md"

    if not src.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Command not found: {command_name}")
        ui.pause("Press Enter to return…")
        return

    shutil.copy2(src, dst)
    print(f"{ui.GREEN}ENABLED{ui.RESET} Command: /{command_name}")
    print(f"  → {dst}")
    ui.pause("Press Enter to return to menu…")


def disable_command(paths: ToolPaths, command_name: str | None = None) -> None:
    active_dir = paths.claude_dir / "commands"

    if not active_dir.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Commands directory not found: {active_dir}")
        ui.pause("Press Enter to return…")
        return

    if not command_name:
        command_name = _select_markdown(paths, active_dir, "Select command to disable:")
    if not command_name:
        return

    dst = active_dir / f"{command_name}.md"

    if not dst.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Command not active: {command_name}")
        ui.pause("Press Enter to return…")
        return

    if ui.prompt_yes_no(f"Disable command /{command_name}?", default=False):
        dst.unlink()
        print(f"{ui.YELLOW}DISABLED{ui.RESET} Command: /{command_name}")
    else:
        print(f"{ui.DIM}Cancelled{ui.RESET}")

    ui.pause("Press Enter to return to menu…")


def enable_agent(paths: ToolPaths, agent_name: str | None = None) -> None:
    available_dir = paths.resources_dir / "claude" / "available-agents"
    active_dir = paths.claude_dir / "agents"
    active_dir.mkdir(parents=True, exist_ok=True)

    if not agent_name:
        agent_name = _select_markdown(paths, available_dir, "Select agent to enable:")
    if not agent_name:
        return

    src = available_dir / f"{agent_name}.md"
    dst = active_dir / f"{agent_name}.md"

    if not src.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Agent not found: {agent_name}")
        ui.pause("Press Enter to return…")
        return

    shutil.copy2(src, dst)
    print(f"{ui.GREEN}ENABLED{ui.RESET} Agent: {agent_name}")
    print(f"  → {dst}")
    ui.pause("Press Enter to return to menu…")


def disable_agent(paths: ToolPaths, agent_name: str | None = None) -> None:
    active_dir = paths.claude_dir / "agents"

    if not active_dir.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Agents directory not found: {active_dir}")
        ui.pause("Press Enter to return…")
        return

    if not agent_name:
        agent_name = _select_markdown(paths, active_dir, "Select agent to disable:")
    if not agent_name:
        return

    dst = active_dir / f"{agent_name}.md"

    if not dst.exists():
        print(f"{ui.RED}ERROR{ui.RESET} Agent not active: {agent_name}")
        ui.pause("Press Enter to return…")
        return

    if ui.prompt_yes_no(f"Disable agent {agent_name}?", default=False):
        dst.unlink()
        print(f"{ui.YELLOW}DISABLED{ui.RESET} Agent: {agent_name}")
    else:
        print(f"{ui.DIM}Cancelled{ui.RESET}")

    ui.pause("Press Enter to return to menu…")


def manage_commands(paths: ToolPaths) -> None:
    while True:
        choices = [
            "List all commands",
            "Enable command",
            "Disable command",
            "Back to main menu",
        ]
        idx = ui.interactive_select("Manage Commands", choices, default_index=0)
        if idx is None or choices[idx] == "Back to main menu":
            return

        ui.clear_screen()
        if choices[idx] == "List all commands":
            list_available_commands(paths)
        elif choices[idx] == "Enable command":
            enable_command(paths)
        elif choices[idx] == "Disable command":
            disable_command(paths)


def manage_agents(paths: ToolPaths) -> None:
    while True:
        choices = [
            "List all agents",
            "Enable agent",
            "Disable agent",
            "Back to main menu",
        ]
        idx = ui.interactive_select("Manage Agents", choices, default_index=0)
        if idx is None or choices[idx] == "Back to main menu":
            return

        ui.clear_screen()
        if choices[idx] == "List all agents":
            list_available_agents(paths)
        elif choices[idx] == "Enable agent":
            enable_agent(paths)
        elif choices[idx] == "Disable agent":
            disable_agent(paths)


def enable_workflow(paths: ToolPaths) -> None:
    print(f"{ui.BOLD}Enabling Workflow Automation{ui.RESET}\n")

    workflow_commands = ["start", "spec", "code", "review", "test", "done", "workflow"]
    print("Enabling workflow commands:")
    for cmd in workflow_commands:
        src = paths.resources_dir / "claude" / "available-commands" / f"{cmd}.md"
        dst = paths.claude_dir / "commands" / f"{cmd}.md"
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  {ui.GREEN}✓{ui.RESET} /{cmd}")
        else:
            print(f"  {ui.RED}✗{ui.RESET} /{cmd} (not found)")

    workflow_agents = [
        "spec-writer",
        "code-implementer",
        "test-writer",
        "workflow-orchestrator",
    ]
    print("\nEnabling workflow agents:")
    for agent in workflow_agents:
        src = paths.resources_dir / "claude" / "available-agents" / f"{agent}.md"
        dst = paths.claude_dir / "agents" / f"{agent}.md"
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  {ui.GREEN}✓{ui.RESET} {agent}")
        else:
            print(f"  {ui.RED}✗{ui.RESET} {agent} (not found)")

    print(f"\n{ui.GREEN}Workflow automation enabled!{ui.RESET}")
    print("\nYou can now use:")
    print("  /start   - Start feature development")
    print("  /spec    - Create technical spec")
    print("  /code    - Implement code")
    print("  /review  - Review code")
    print("  /test    - Create and run tests")
    print("  /done    - Complete feature")
    print("  /workflow - Run complete workflow")

    ui.pause("\nPress Enter to return to menu…")


# def run_menu(paths: ToolPaths) -> None:
#     options = [
#         "Init project",
#         "Setup VSCode",
#         "Setup AI Agent",
#         "Manage Commands",
#         "Manage Agents",
#         "Enable Workflow",
#         "Verify",
#         "Exit",
#     ]

#     actions: Iterable[Callable[[], None]] = [
#         lambda: init_project(paths),
#         lambda: setup_vscode(paths),
#         lambda: setup_ai_agent(paths),
#         lambda: manage_commands(paths),
#         lambda: manage_agents(paths),
#         lambda: enable_workflow(paths),
#         lambda: verify(paths),
#         _exit_app,
#     ]

#     ui.menu_loop(options, list(actions))


# def _exit_app() -> None:
#     ui.clear_screen()
#     sys.exit(0)


# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents/",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
    },
    "shai": {
        "name": "SHAI",
        "folder": ".shai/",
        "install_url": "https://github.com/ovh/shai",
        "requires_cli": True,
    },
    "bob": {
        "name": "IBM Bob",
        "folder": ".bob/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
}


def is_x100_project(path: Path) -> bool:
    """Check if the given path is an x100 project (contains .x100 folder)."""
    x100_dir = path / ".x100"
    if not x100_dir.is_dir():
        return False

    config_file = x100_dir / "config.json"
    if not config_file.is_file():
        return False

    return True
