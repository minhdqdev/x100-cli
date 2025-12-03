"""Data models for nextstep analysis."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any


@dataclass
class TodoItem:
    """A TODO or FIXME marker in the code."""
    
    file: Path
    line: int
    text: str
    type: str  # 'TODO' or 'FIXME'
    age_days: Optional[int] = None


@dataclass
class CodeAnalysis:
    """Results of codebase analysis."""
    
    file_count: int
    line_count: int
    python_files: int = 0
    javascript_files: int = 0
    other_files: int = 0
    todos: List[TodoItem] = field(default_factory=list)
    fixmes: List[TodoItem] = field(default_factory=list)
    test_coverage: Optional[float] = None
    last_commit_date: Optional[datetime] = None
    recent_commit_count: int = 0
    untested_files: List[Path] = field(default_factory=list)


@dataclass
class GitAnalysis:
    """Results of git history analysis."""
    
    commit_count_7d: int
    commit_count_30d: int
    active_branches: int
    contributors: int
    last_commit_date: Optional[datetime] = None
    last_commit_message: Optional[str] = None
    commits_per_day: float = 0.0
    is_git_repo: bool = True


@dataclass
class TestAnalysis:
    """Results of test coverage analysis."""
    
    coverage_percentage: Optional[float] = None
    test_count: int = 0
    untested_files: List[Path] = field(default_factory=list)
    test_files: List[Path] = field(default_factory=list)


@dataclass
class IssueInfo:
    """GitHub issue information."""
    
    number: int
    title: str
    state: str
    created_days_ago: int
    labels: List[str] = field(default_factory=list)
    is_blocked: bool = False


@dataclass
class ProjectStatus:
    """Project management status."""
    
    open_issues: List[IssueInfo] = field(default_factory=list)
    blocked_issues: List[IssueInfo] = field(default_factory=list)
    stale_issues: List[IssueInfo] = field(default_factory=list)
    open_pr_count: int = 0
    stale_pr_count: int = 0


@dataclass
class Gap:
    """A gap or inconsistency found in the project."""
    
    category: str
    description: str
    severity: str  # 'low', 'medium', 'high'
    file: Optional[Path] = None


@dataclass
class Blocker:
    """A blocking issue."""
    
    title: str
    impact: str
    source: str  # 'code', 'github', 'git'
    details: str = ""


@dataclass
class NextStep:
    """A recommended next step."""
    
    priority: str  # 'NOW', 'This Week', 'Next Sprint'
    action: str
    rationale: str
    impact: str
    effort: str
    order: int = 0


@dataclass
class HealthScore:
    """Project health metrics."""
    
    overall: int  # 0-100
    velocity_score: int = 0
    quality_score: int = 0
    blocker_score: int = 0
    activity_score: int = 0
    summary: str = ""
    trend: str = ""  # 'improving', 'stable', 'declining'


@dataclass
class Recommendations:
    """Complete analysis recommendations."""
    
    health_score: HealthScore
    blockers: List[Blocker] = field(default_factory=list)
    gaps: List[Gap] = field(default_factory=list)
    next_steps: List[NextStep] = field(default_factory=list)
    raw_analysis: str = ""
