"""AI client integrations for nextstep analysis."""

import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class AIClient(ABC):
    """Base class for AI client integrations."""
    
    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """Send prompt to AI and return response."""
        pass


class ClaudeClient(AIClient):
    """Claude Code CLI client."""
    
    def analyze(self, prompt: str) -> str:
        """Use Claude Code CLI to analyze."""
        try:
            result = subprocess.run(
                ["claude", "chat", "-m", prompt],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
        except FileNotFoundError:
            return "Error: Claude CLI not found. Install from: https://docs.anthropic.com/en/docs/claude-code/setup"
        except subprocess.TimeoutExpired:
            return "Error: Claude CLI timed out after 60 seconds"
        except Exception as e:
            return f"Error: {str(e)}"


class CopilotClient(AIClient):
    """GitHub Copilot CLI client."""
    
    def analyze(self, prompt: str) -> str:
        """Use GitHub Copilot CLI to analyze."""
        try:
            # Use the correct copilot command with -p flag
            result = subprocess.run(
                ["copilot", "-p", prompt, "--allow-all-tools"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
        except FileNotFoundError:
            return "Error: GitHub Copilot CLI not found. Install from: https://github.com/features/copilot/cli"
        except subprocess.TimeoutExpired:
            return "Error: GitHub Copilot CLI timed out after 60 seconds"
        except Exception as e:
            return f"Error: {str(e)}"


class GeminiClient(AIClient):
    """Gemini CLI client."""
    
    def analyze(self, prompt: str) -> str:
        """Use Gemini CLI to analyze."""
        try:
            result = subprocess.run(
                ["gemini", "chat", prompt],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
        except FileNotFoundError:
            return "Error: Gemini CLI not found. Install from: https://github.com/google-gemini/gemini-cli"
        except subprocess.TimeoutExpired:
            return "Error: Gemini CLI timed out after 60 seconds"
        except Exception as e:
            return f"Error: {str(e)}"


class FallbackClient(AIClient):
    """Fallback client when AI CLI is not available."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
    
    def analyze(self, prompt: str) -> str:
        """Return a message indicating fallback to rule-based analysis."""
        return "Using rule-based analysis (AI CLI not available)"


def get_ai_client(agent_name: str) -> AIClient:
    """Get appropriate AI client based on agent name."""
    clients = {
        "claude": ClaudeClient,
        "copilot": CopilotClient,
        "gemini": GeminiClient,
    }
    
    client_class = clients.get(agent_name)
    if client_class:
        return client_class()
    else:
        # For agents without CLI integration, use fallback
        return FallbackClient(agent_name)


def build_analysis_prompt(
    code_analysis,
    git_analysis,
    test_analysis,
    project_status=None,
    story_statuses=None,
    doc_status=None,
) -> str:
    """Build a comprehensive prompt for AI analysis."""
    
    prompt_parts = [
        "# Project Analysis Request",
        "",
        "You are an AI Project Manager/Tech Lead. Analyze the following project data and provide actionable recommendations.",
        "",
        "## Codebase Metrics",
        f"- Total files: {code_analysis.file_count}",
        f"- Total lines: {code_analysis.line_count}",
        f"- TODO markers: {len(code_analysis.todos)}",
        f"- FIXME markers: {len(code_analysis.fixmes)}",
        "",
        "## Git Activity",
    ]
    
    if git_analysis.is_git_repo:
        prompt_parts.extend([
            f"- Commits (last 7 days): {git_analysis.commit_count_7d}",
            f"- Commits (last 30 days): {git_analysis.commit_count_30d}",
            f"- Commits per day: {git_analysis.commits_per_day:.2f}",
            f"- Active branches: {git_analysis.active_branches}",
            f"- Contributors: {git_analysis.contributors}",
            f"- Last commit: {git_analysis.last_commit_date}",
        ])
    else:
        prompt_parts.append("- Not a git repository")
    
    prompt_parts.extend([
        "",
        "## Test Coverage",
    ])
    
    if test_analysis.coverage_percentage is not None:
        prompt_parts.append(f"- Coverage: {test_analysis.coverage_percentage}%")
    else:
        prompt_parts.append("- Coverage: Not available")
    
    if test_analysis.untested_files:
        prompt_parts.append(f"- Untested files: {len(test_analysis.untested_files)}")
        # List high-risk untested files
        high_risk = [
            f for f in test_analysis.untested_files
            if any(keyword in str(f).lower() for keyword in ['auth', 'payment', 'security', 'api'])
        ]
        if high_risk:
            prompt_parts.append("- High-risk untested files:")
            for f in high_risk[:5]:
                prompt_parts.append(f"  * {f.name}")
    
    if story_statuses:
        prompt_parts.extend([
            "",
            "## User Stories",
            f"- Total stories: {len(story_statuses)}",
        ])
        done_no_impl = [s for s in story_statuses if s.status == 'done' and not s.has_implementation]
        if done_no_impl:
            prompt_parts.append(f"- Stories marked done without implementation: {len(done_no_impl)}")
    
    if doc_status:
        prompt_parts.extend([
            "",
            "## Documentation Status",
            f"- Has README: {doc_status.has_readme}",
            f"- Has LICENSE: {doc_status.has_license}",
            f"- Has CHANGELOG: {doc_status.has_changelog}",
        ])
        if doc_status.outdated_docs:
            prompt_parts.append(f"- Docs with TODO/TBD: {len(doc_status.outdated_docs)}")
    
    prompt_parts.extend([
        "",
        "## Request",
        "",
        "Based on this data, provide:",
        "1. Top 3 most critical issues or blockers",
        "2. Top 3 recommended next steps (prioritized)",
        "3. Overall project health assessment (0-100 score)",
        "4. Key risks or concerns",
        "",
        "Keep responses concise and actionable. Focus on immediate priorities.",
    ])
    
    return "\n".join(prompt_parts)
