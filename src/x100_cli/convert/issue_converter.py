"""Issue converter implementation."""

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .schemas import GitHubIssueSchema, get_schema_prompt
from ..core import AGENT_CONFIG, load_config


console = Console()


@dataclass
class ConversionResult:
    """Result of a user story conversion."""

    file_path: Path
    success: bool
    issue_data: Optional[GitHubIssueSchema] = None
    issue_url: Optional[str] = None
    error_message: Optional[str] = None


class IssueConverter:
    """Converts user stories to GitHub issues."""

    US_PATTERN = re.compile(r"^US-\d+-[a-zA-Z0-9\-]+\.md$")

    def __init__(self, agent_name: Optional[str] = None):
        """
        Initialize the converter.

        Args:
            agent_name: Name of AI agent to use. If None, uses default from config.
        """
        self.agent_name = agent_name or self._get_default_agent()
        self.agent_config = AGENT_CONFIG.get(self.agent_name)

        if not self.agent_config:
            raise ValueError(f"Unknown agent: {self.agent_name}")

        # Map agent names to their CLI commands (some differ from agent key)
        self.cli_command = self._get_cli_command()

        # Verify agent CLI is available
        if not self._check_agent_cli():
            install_url = self.agent_config.get("install_url")
            raise RuntimeError(
                f"{self.agent_config['name']} CLI not found. "
                f"Install from: {install_url if install_url else 'check agent documentation'}"
            )

    def _get_cli_command(self) -> str:
        """Get the CLI command for the agent."""
        # Map agent names to CLI commands (for cases where they differ)
        cli_commands = {
            "copilot": "copilot",
            "claude": "claude",
            "gemini": "gemini",
            "cursor-agent": "cursor-agent",
            "qwen": "qwen",
            "opencode": "opencode",
            "codex": "codex",
            "auggie": "auggie",
            "codebuddy": "codebuddy",
            "amp": "amp",
            "shai": "shai",
            "q": "q",
        }
        return cli_commands.get(self.agent_name, self.agent_name)

    def _get_default_agent(self) -> str:
        """Get the default agent from project config."""
        config = load_config()
        return config.get("default_agent", "claude")

    def _check_agent_cli(self) -> bool:
        """Check if the agent CLI tool is available."""
        try:
            # Special handling for different CLIs
            if self.cli_command == "copilot":
                # Copilot CLI uses `copilot --version`
                result = subprocess.run(
                    [self.cli_command, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            else:
                result = subprocess.run(
                    [self.cli_command, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _is_user_story_file(self, file_path: Path) -> bool:
        """Check if a file matches the user story naming pattern."""
        return bool(self.US_PATTERN.match(file_path.name))

    def _find_user_story_files(self, path: Path) -> List[Path]:
        """
        Find all user story files in the given path.

        Args:
            path: Either a single file or a directory

        Returns:
            List of user story file paths
        """
        if path.is_file():
            if self._is_user_story_file(path):
                return [path]
            else:
                console.print(
                    f"[yellow]Warning:[/yellow] File {path.name} does not match pattern US-[number]-[slug].md"
                )
                return []

        elif path.is_dir():
            # Find all matching files in directory (non-recursive)
            files = [
                f for f in path.iterdir() if f.is_file() and self._is_user_story_file(f)
            ]
            return sorted(files)

        else:
            return []

    def _convert_all_with_ai(
        self, us_files: List[Path], temp_dir: Path
    ) -> Tuple[bool, dict, Optional[str]]:
        """
        Use AI agent to convert all user story markdown files to JSON in a single prompt.

        Args:
            us_files: List of user story markdown files
            temp_dir: Temporary directory for output

        Returns:
            Tuple of (success, filename_to_json_dict, error_message)
        """
        if not us_files:
            return False, {}, "No files to convert"

        # Build combined prompt with all user stories
        prompt_parts = [get_schema_prompt()]
        prompt_parts.append(
            "\nConvert the following user story files to JSON objects following the schema above."
        )
        prompt_parts.append(
            "Return a JSON object where keys are filenames (without .md extension) and values are the converted issue objects."
        )
        prompt_parts.append("\nExample output format:")
        prompt_parts.append(
            '{\n  "US-001-example": { "title": "...", "body": "...", ... },'
        )
        prompt_parts.append(
            '  "US-002-another": { "title": "...", "body": "...", ... }\n}'
        )
        prompt_parts.append("\n---\n")

        for us_file in us_files:
            try:
                us_content = us_file.read_text(encoding="utf-8")
                file_stem = us_file.stem  # filename without extension
                prompt_parts.append(f"\n### FILE: {us_file.name}\n")
                prompt_parts.append(us_content)
                prompt_parts.append("\n---\n")
            except Exception as e:
                return False, {}, f"Failed to read {us_file.name}: {e}"

        prompt = "\n".join(prompt_parts)

        # Call AI agent
        try:
            result = None
            timeout_seconds = 600  # 10 minutes timeout for batch processing
            
            if self.agent_name == "copilot":
                result = subprocess.run(
                    [self.cli_command, "--prompt", prompt, "--allow-all-tools"],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                )
            elif self.agent_name == "claude":
                result = subprocess.run(
                    ["claude"],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                )
            elif self.agent_name in ["gemini", "qwen"]:
                result = subprocess.run(
                    [self.cli_command, prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                )
            elif self.agent_name in [
                "opencode",
                "codex",
                "auggie",
                "codebuddy",
                "amp",
                "shai",
            ]:
                result = subprocess.run(
                    [self.cli_command, "--prompt", prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                )
            elif self.agent_name == "q":
                result = subprocess.run(
                    ["q", "generate", "--prompt", prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                )
            else:
                return False, {}, f"Unsupported agent: {self.agent_name}"

            if result.returncode != 0:
                error_msg = (
                    result.stderr.strip() or result.stdout.strip() or "Unknown error"
                )
                return False, {}, f"AI conversion failed: {error_msg}"

            # Extract and parse JSON response
            response_text = result.stdout.strip()
            json_text = self._extract_json_from_response(response_text)

            try:
                all_issues = json.loads(json_text)

                # Validate it's a dictionary
                if not isinstance(all_issues, dict):
                    return (
                        False,
                        {},
                        "AI response is not a JSON object with filename keys",
                    )

                # Validate each issue has required fields
                for filename, issue_data in all_issues.items():
                    if not isinstance(issue_data, dict):
                        return (
                            False,
                            {},
                            f"Issue data for {filename} is not a JSON object",
                        )
                    if "title" not in issue_data or "body" not in issue_data:
                        return (
                            False,
                            {},
                            f"Issue for {filename} missing required fields (title, body)",
                        )

                # Write individual JSON files for compatibility
                for us_file in us_files:
                    file_stem = us_file.stem
                    if file_stem in all_issues:
                        json_file = temp_dir / f"{file_stem}.json"
                        json_file.write_text(
                            json.dumps(all_issues[file_stem], indent=2),
                            encoding="utf-8",
                        )

                return True, all_issues, None

            except json.JSONDecodeError as e:
                return False, {}, f"Invalid JSON in AI response: {e}"

        except subprocess.TimeoutExpired:
            return False, {}, "AI conversion timed out (600s)"
        except Exception as e:
            return False, {}, f"Unexpected error: {e}"

    def _convert_with_ai(
        self, us_file: Path, temp_dir: Path
    ) -> Tuple[bool, Optional[Path], Optional[str]]:
        """
        Use AI agent to convert user story markdown to JSON (legacy single-file method).

        Args:
            us_file: Path to user story markdown file
            temp_dir: Temporary directory for output

        Returns:
            Tuple of (success, json_file_path, error_message)
        """
        # Read user story content
        try:
            us_content = us_file.read_text(encoding="utf-8")
        except Exception as e:
            return False, None, f"Failed to read file: {e}"

        # Prepare prompt for AI
        prompt = f"""
{get_schema_prompt()}

USER STORY FILE: {us_file.name}

USER STORY CONTENT:
{us_content}

Convert this user story to a JSON object following the schema above.
"""

        # Create output file path
        json_file = temp_dir / f"{us_file.stem}.json"

        # Call AI agent (implementation depends on specific agent)
        try:
            if self.agent_name == "copilot":
                # GitHub Copilot CLI: copilot --prompt "prompt" --allow-all-tools
                # Output is captured from stdout
                result = subprocess.run(
                    [self.cli_command, "--prompt", prompt, "--allow-all-tools"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                # Write output to json file since copilot outputs to stdout
                if result.returncode == 0:
                    json_file.write_text(result.stdout, encoding="utf-8")
            elif self.agent_name == "claude":
                # Claude CLI: echo prompt | claude --output file
                result = subprocess.run(
                    ["claude", "--output", str(json_file)],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            elif self.agent_name in ["gemini", "qwen"]:
                # Gemini/Qwen CLI: agent "prompt" --output file
                result = subprocess.run(
                    [self.cli_command, prompt, "--output", str(json_file)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            elif self.agent_name in [
                "opencode",
                "codex",
                "auggie",
                "codebuddy",
                "amp",
                "shai",
            ]:
                # Generic CLI pattern: agent --prompt "prompt" --output file
                result = subprocess.run(
                    [self.cli_command, "--prompt", prompt, "--output", str(json_file)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            elif self.agent_name == "q":
                # Amazon Q Developer CLI
                result = subprocess.run(
                    ["q", "generate", "--prompt", prompt, "--output", str(json_file)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            else:
                return False, None, f"Unsupported agent: {self.agent_name}"

            if result.returncode != 0:
                error_msg = (
                    result.stderr.strip() or result.stdout.strip() or "Unknown error"
                )
                return False, None, f"AI conversion failed: {error_msg}"

            # Verify JSON file was created
            if not json_file.exists():
                return False, None, "AI did not generate output file"

            # Try to parse JSON to validate
            try:
                json_content = json_file.read_text(encoding="utf-8")
                # Clean up potential markdown code blocks
                json_content = self._extract_json_from_response(json_content)
                json_data = json.loads(json_content)

                # Validate required fields
                if "title" not in json_data or "body" not in json_data:
                    return (
                        False,
                        None,
                        "Generated JSON missing required fields (title, body)",
                    )

                # Write cleaned JSON back
                json_file.write_text(json.dumps(json_data, indent=2), encoding="utf-8")

            except json.JSONDecodeError as e:
                return False, None, f"Invalid JSON generated: {e}"

            return True, json_file, None

        except subprocess.TimeoutExpired:
            return False, None, "AI conversion timed out (60s)"
        except Exception as e:
            return False, None, f"Unexpected error: {e}"

    def _extract_json_from_response(self, text: str) -> str:
        """Extract JSON from AI response that may contain markdown code blocks."""
        # Remove markdown code blocks if present
        text = text.strip()

        # Check for ```json ... ``` or ``` ... ```
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)

        return text.strip()

    def _create_github_issue(
        self,
        issue_data: GitHubIssueSchema,
        repo: Optional[str] = None,
        project_id: Optional[int] = None,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create a GitHub issue using gh CLI.

        Args:
            issue_data: Issue data to create
            repo: Repository in format "owner/repo" (optional, uses current repo if None)
            project_id: GitHub project ID to link to (optional)

        Returns:
            Tuple of (success, issue_url, error_message)
        """
        try:
            # Build gh issue create command
            cmd = ["gh", "issue", "create"]

            if repo:
                cmd.extend(["--repo", repo])

            cmd.extend(["--title", issue_data.title, "--body", issue_data.body])

            # Add assignees (skip labels to avoid errors with non-existent labels)
            if issue_data.assignees:
                for assignee in issue_data.assignees:
                    cmd.extend(["--assignee", assignee])

            # Add milestone
            if issue_data.milestone:
                cmd.extend(["--milestone", str(issue_data.milestone)])

            # Create the issue without labels first
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                error_msg = (
                    result.stderr.strip() or result.stdout.strip() or "Unknown error"
                )
                return False, None, f"Failed to create issue: {error_msg}"

            # Extract issue URL from output
            issue_url = result.stdout.strip()

            # Try to add labels separately (ignore failures)
            if issue_data.labels and issue_url:
                issue_num = issue_url.rstrip("/").split("/")[-1]
                for label in issue_data.labels:
                    label_cmd = ["gh", "issue", "edit", issue_num, "--add-label", label]
                    if repo:
                        label_cmd.extend(["--repo", repo])
                    # Run but ignore errors if label doesn't exist
                    subprocess.run(
                        label_cmd, capture_output=True, text=True, timeout=10
                    )

            # Link to project if configured
            if project_id and issue_url:
                # Extract owner from repo or issue URL
                owner = None
                if repo:
                    # Format: "owner/repo"
                    owner = repo.split("/")[0]
                else:
                    # Extract from issue URL: https://github.com/owner/repo/issues/123
                    import re

                    url_match = re.search(r"github\.com/([^/]+)/", issue_url)
                    if url_match:
                        owner = url_match.group(1)

                # Add to project using gh CLI
                project_cmd = [
                    "gh",
                    "project",
                    "item-add",
                    str(project_id),
                    "--url",
                    issue_url,
                ]

                # Add owner for organization projects
                if owner:
                    project_cmd.extend(["--owner", owner])

                project_result = subprocess.run(
                    project_cmd, capture_output=True, text=True, timeout=30
                )

                if project_result.returncode != 0:
                    console.print(
                        f"[yellow]Warning:[/yellow] Created issue but failed to link to project: "
                        f"{project_result.stderr.strip()}"
                    )

            return True, issue_url, None

        except subprocess.TimeoutExpired:
            return False, None, "GitHub issue creation timed out (30s)"
        except Exception as e:
            return False, None, f"Unexpected error: {e}"

    def convert_and_create(
        self, path: Path, repo: Optional[str] = None, project_id: Optional[int] = None
    ) -> List[ConversionResult]:
        """
        Convert user stories and create GitHub issues.

        Args:
            path: Path to user story file or directory
            repo: GitHub repository in format "owner/repo" (optional)
            project_id: GitHub project ID to link issues to (optional)

        Returns:
            List of conversion results
        """
        # Find user story files
        us_files = self._find_user_story_files(path)

        if not us_files:
            console.print(
                f"[yellow]No user story files found matching pattern US-[number]-[slug].md[/yellow]"
            )
            return []

        console.print(
            f"[cyan]Found {len(us_files)} user story file(s) to convert[/cyan]\n"
        )

        results: List[ConversionResult] = []
        BATCH_SIZE = 10

        # Create temp directory for JSON files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:

                # Process files in batches of 10
                all_converted_issues = {}

                for batch_idx in range(0, len(us_files), BATCH_SIZE):
                    batch_files = us_files[batch_idx : batch_idx + BATCH_SIZE]
                    batch_num = (batch_idx // BATCH_SIZE) + 1
                    total_batches = (len(us_files) + BATCH_SIZE - 1) // BATCH_SIZE

                    convert_task = progress.add_task(
                        f"Converting batch {batch_num}/{total_batches} ({len(batch_files)} files) with AI...",
                        total=None,
                    )

                    batch_success, batch_issues, batch_error = (
                        self._convert_all_with_ai(batch_files, temp_path)
                    )

                    progress.remove_task(convert_task)

                    if not batch_success:
                        # If batch conversion fails, mark all files in batch as failed
                        for us_file in batch_files:
                            results.append(
                                ConversionResult(
                                    file_path=us_file,
                                    success=False,
                                    error_message=batch_error
                                    or f"Batch {batch_num} conversion failed",
                                )
                            )
                    else:
                        # Store successfully converted issues
                        all_converted_issues.update(batch_issues)

                # Now create GitHub issues for all successfully converted files
                for us_file in us_files:
                    file_stem = us_file.stem

                    # Skip if already marked as failed
                    if any(r.file_path == us_file and not r.success for r in results):
                        continue

                    if file_stem not in all_converted_issues:
                        results.append(
                            ConversionResult(
                                file_path=us_file,
                                success=False,
                                error_message=f"AI did not return data for {us_file.name}",
                            )
                        )
                        continue

                    # Parse issue data
                    try:
                        issue_data = GitHubIssueSchema.from_dict(
                            all_converted_issues[file_stem]
                        )
                    except Exception as e:
                        results.append(
                            ConversionResult(
                                file_path=us_file,
                                success=False,
                                error_message=f"Failed to parse issue data: {e}",
                            )
                        )
                        continue

                    # Create GitHub issue
                    task = progress.add_task(
                        f"Creating issue for {us_file.name}...", total=None
                    )

                    issue_success, issue_url, issue_error = self._create_github_issue(
                        issue_data, repo=repo, project_id=project_id
                    )

                    progress.remove_task(task)

                    if issue_success:
                        results.append(
                            ConversionResult(
                                file_path=us_file,
                                success=True,
                                issue_data=issue_data,
                                issue_url=issue_url,
                            )
                        )
                    else:
                        results.append(
                            ConversionResult(
                                file_path=us_file,
                                success=False,
                                issue_data=issue_data,
                                error_message=f"Issue creation failed: {issue_error}",
                            )
                        )

        return results

    @staticmethod
    def display_results(results: List[ConversionResult]) -> None:
        """Display conversion results in a formatted table."""
        if not results:
            console.print("[yellow]No results to display[/yellow]")
            return

        success_count = sum(1 for r in results if r.success)
        failure_count = len(results) - success_count

        # Summary
        console.print()
        if success_count == len(results):
            summary_color = "green"
            emoji = "🎉"
        elif success_count > 0:
            summary_color = "yellow"
            emoji = "⚠️"
        else:
            summary_color = "red"
            emoji = "❌"

        summary_panel = Panel(
            f"[bold]Converted:[/bold] {success_count}/{len(results)} user stories\n"
            f"[bold]Succeeded:[/bold] {success_count}\n"
            f"[bold]Failed:[/bold] {failure_count}",
            title=f"{emoji} Conversion Summary",
            border_style=summary_color,
        )
        console.print(summary_panel)
        console.print()

        # Detailed results
        table = Table(title="Detailed Results")
        table.add_column("File", style="cyan", no_wrap=False)
        table.add_column("Status", style="white")
        table.add_column("Details", style="white", no_wrap=False)

        for result in results:
            if result.success:
                status = "[green]✓ Success[/green]"
                details = f"[dim]{result.issue_url}[/dim]" if result.issue_url else ""
            else:
                status = "[red]✗ Failed[/red]"
                details = (
                    f"[red]{result.error_message}[/red]" if result.error_message else ""
                )

            table.add_row(result.file_path.name, status, details)

        console.print(table)

    @staticmethod
    def prompt_cleanup(results: List[ConversionResult]) -> None:
        """Prompt user to delete successfully converted files."""
        successful_files = [r.file_path for r in results if r.success]

        if not successful_files:
            return

        console.print()
        console.print(
            f"[cyan]{len(successful_files)} file(s) were successfully converted to GitHub issues.[/cyan]"
        )
        console.print(
            "[dim]You can now safely delete these user story files if desired.[/dim]"
        )

        try:
            response = (
                input("\nDelete successfully converted files? [y/N]: ").strip().lower()
            )

            if response in ["y", "yes"]:
                deleted_count = 0
                for file_path in successful_files:
                    try:
                        file_path.unlink()
                        console.print(f"[green]✓[/green] Deleted: {file_path.name}")
                        deleted_count += 1
                    except Exception as e:
                        console.print(
                            f"[red]✗[/red] Failed to delete {file_path.name}: {e}"
                        )

                console.print(
                    f"\n[green]Deleted {deleted_count}/{len(successful_files)} file(s)[/green]"
                )
            else:
                console.print(
                    "[dim]Files kept - you can delete them manually later[/dim]"
                )

        except KeyboardInterrupt:
            console.print("\n[yellow]Cleanup cancelled[/yellow]")
