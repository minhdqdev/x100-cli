"""Git analyzer for repository history analysis."""

from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import subprocess

from ..models import GitAnalysis


class GitAnalyzer:
    """Analyze git repository history and activity."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
    
    def analyze(self) -> GitAnalysis:
        """Perform complete git analysis."""
        if not self._is_git_repo():
            return GitAnalysis(
                commit_count_7d=0,
                commit_count_30d=0,
                active_branches=0,
                contributors=0,
                is_git_repo=False,
            )
        
        commit_count_7d = self._count_commits_since(days=7)
        commit_count_30d = self._count_commits_since(days=30)
        active_branches = self._count_branches()
        contributors = self._count_contributors()
        last_commit_date = self._get_last_commit_date()
        last_commit_message = self._get_last_commit_message()
        
        commits_per_day = commit_count_7d / 7.0 if commit_count_7d > 0 else 0.0
        
        return GitAnalysis(
            commit_count_7d=commit_count_7d,
            commit_count_30d=commit_count_30d,
            active_branches=active_branches,
            contributors=contributors,
            last_commit_date=last_commit_date,
            last_commit_message=last_commit_message,
            commits_per_day=round(commits_per_day, 1),
            is_git_repo=True,
        )
    
    def _is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        git_dir = self.repo_path / ".git"
        return git_dir.exists()
    
    def _run_git_command(self, args: list[str]) -> Optional[str]:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def _count_commits_since(self, days: int) -> int:
        """Count commits in the last N days."""
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        output = self._run_git_command(['rev-list', '--count', '--since', since_date, 'HEAD'])
        if output:
            try:
                return int(output)
            except ValueError:
                pass
        return 0
    
    def _count_branches(self) -> int:
        """Count number of branches."""
        output = self._run_git_command(['branch', '-a'])
        if output:
            return len([line for line in output.split('\n') if line.strip()])
        return 0
    
    def _count_contributors(self) -> int:
        """Count unique contributors."""
        output = self._run_git_command(['shortlog', '-s', '-n', 'HEAD'])
        if output:
            return len(output.split('\n'))
        return 0
    
    def _get_last_commit_date(self) -> Optional[datetime]:
        """Get date of last commit."""
        output = self._run_git_command(['log', '-1', '--format=%ct'])
        if output:
            try:
                timestamp = int(output)
                return datetime.fromtimestamp(timestamp)
            except ValueError:
                pass
        return None
    
    def _get_last_commit_message(self) -> Optional[str]:
        """Get last commit message."""
        output = self._run_git_command(['log', '-1', '--format=%s'])
        return output if output else None
