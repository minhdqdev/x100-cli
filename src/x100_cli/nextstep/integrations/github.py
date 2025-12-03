"""GitHub integration for project management."""

from datetime import datetime
from typing import Optional

from ..models import ProjectStatus, IssueInfo


class GitHubIntegration:
    """Integration with GitHub Issues and Projects."""
    
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self._gh = None
        self._repo = None
    
    def _init_github(self):
        """Lazy initialize GitHub client."""
        if self._gh is None:
            try:
                import github
                self._gh = github.Github(self.token)
                self._repo = self._gh.get_repo(self.repo)
            except ImportError:
                raise ImportError(
                    "PyGithub is required for GitHub integration. "
                    "Install with: pip install PyGithub"
                )
            except Exception as e:
                raise Exception(f"Failed to connect to GitHub: {e}")
    
    def get_project_status(self) -> ProjectStatus:
        """Get GitHub project status."""
        self._init_github()
        
        open_issues = []
        blocked_issues = []
        stale_issues = []
        
        # Get open issues
        for issue in self._repo.get_issues(state='open'):
            days_ago = (datetime.now() - issue.created_at.replace(tzinfo=None)).days
            
            labels = [label.name for label in issue.labels]
            is_blocked = 'blocked' in labels or 'blocker' in labels
            is_stale = days_ago > 30
            
            issue_info = IssueInfo(
                number=issue.number,
                title=issue.title,
                state=issue.state,
                created_days_ago=days_ago,
                labels=labels,
                is_blocked=is_blocked,
            )
            
            open_issues.append(issue_info)
            
            if is_blocked:
                blocked_issues.append(issue_info)
            
            if is_stale:
                stale_issues.append(issue_info)
        
        # Get PR counts
        open_prs = self._repo.get_pulls(state='open')
        open_pr_count = open_prs.totalCount
        
        stale_pr_count = 0
        for pr in open_prs:
            days_ago = (datetime.now() - pr.created_at.replace(tzinfo=None)).days
            if days_ago > 7:
                stale_pr_count += 1
        
        return ProjectStatus(
            open_issues=open_issues,
            blocked_issues=blocked_issues,
            stale_issues=stale_issues,
            open_pr_count=open_pr_count,
            stale_pr_count=stale_pr_count,
        )
