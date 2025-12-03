"""Output formatters for nextstep analysis."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import (
    Recommendations,
    CodeAnalysis,
    GitAnalysis,
    TestAnalysis,
)


class MarkdownFormatter:
    """Format nextstep analysis as Markdown."""
    
    def format(
        self,
        recommendations: Recommendations,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
        verbose: bool = False,
    ) -> str:
        """Format analysis as Markdown."""
        output = []
        
        # Header
        output.append("# Project Health Analysis")
        output.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Health Score
        health = recommendations.health_score
        output.append("## 📈 Project Health\n")
        output.append(f"**Overall Score:** {health.overall}/100 ({health.summary})\n")
        output.append("| Metric | Score |")
        output.append("|--------|-------|")
        output.append(f"| Velocity | {health.velocity_score}/100 |")
        output.append(f"| Quality | {health.quality_score}/100 |")
        output.append(f"| Blockers | {health.blocker_score}/100 |")
        output.append(f"| Activity | {health.activity_score}/100 |")
        output.append("")
        
        # Statistics
        if verbose:
            output.append("## 📊 Statistics\n")
            output.append("| Metric | Value |")
            output.append("|--------|-------|")
            output.append(f"| Files | {code_analysis.file_count} |")
            output.append(f"| Lines of Code | {code_analysis.line_count:,} |")
            output.append(f"| Python Files | {code_analysis.python_files} |")
            output.append(f"| JavaScript Files | {code_analysis.javascript_files} |")
            output.append(f"| TODO Markers | {len(code_analysis.todos)} |")
            output.append(f"| FIXME Markers | {len(code_analysis.fixmes)} |")
            
            if test_analysis.coverage_percentage:
                output.append(f"| Test Coverage | {test_analysis.coverage_percentage}% |")
            output.append(f"| Test Files | {test_analysis.test_count} |")
            
            if git_analysis.is_git_repo:
                output.append(f"| Commits (7d) | {git_analysis.commit_count_7d} |")
                output.append(f"| Commits (30d) | {git_analysis.commit_count_30d} |")
                output.append(f"| Commits/Day | {git_analysis.commits_per_day} |")
            output.append("")
        
        # Blockers
        if recommendations.blockers:
            output.append("## 🔴 Blockers & Risks\n")
            for blocker in recommendations.blockers:
                output.append(f"### {blocker.title}\n")
                output.append(f"- **Impact:** {blocker.impact}")
                output.append(f"- **Source:** {blocker.source}")
                if blocker.details:
                    output.append(f"- **Details:** {blocker.details}")
                output.append("")
        
        # Gaps
        if recommendations.gaps:
            output.append("## 🔍 Gaps Detected\n")
            for gap in recommendations.gaps:
                severity_icon = "🔴" if gap.severity == "high" else "⚠️"
                output.append(f"- {severity_icon} **{gap.category}:** {gap.description}")
            output.append("")
        
        # Next Steps
        if recommendations.next_steps:
            output.append("## 💡 Recommended Next Steps\n")
            
            # Group by priority
            priorities = ["NOW", "This Week", "Next Sprint"]
            for priority in priorities:
                steps = [s for s in recommendations.next_steps if s.priority == priority]
                if steps:
                    if priority == "NOW":
                        icon = "🎯"
                    elif priority == "This Week":
                        icon = "🔄"
                    else:
                        icon = "📅"
                    
                    output.append(f"### {icon} {priority}\n")
                    for step in steps:
                        output.append(f"{step.order}. **{step.action}**")
                        output.append(f"   - **Rationale:** {step.rationale}")
                        output.append(f"   - **Impact:** {step.impact}")
                        output.append(f"   - **Effort:** {step.effort}")
                        output.append("")
        
        return "\n".join(output)


class JSONFormatter:
    """Format nextstep analysis as JSON."""
    
    def format(
        self,
        recommendations: Recommendations,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
        verbose: bool = False,
    ) -> str:
        """Format analysis as JSON."""
        output = {
            "timestamp": datetime.now().isoformat(),
            "health_score": {
                "overall": recommendations.health_score.overall,
                "summary": recommendations.health_score.summary,
                "velocity": recommendations.health_score.velocity_score,
                "quality": recommendations.health_score.quality_score,
                "blockers": recommendations.health_score.blocker_score,
                "activity": recommendations.health_score.activity_score,
                "trend": recommendations.health_score.trend,
            },
            "blockers": [
                {
                    "title": b.title,
                    "impact": b.impact,
                    "source": b.source,
                    "details": b.details,
                }
                for b in recommendations.blockers
            ],
            "gaps": [
                {
                    "category": g.category,
                    "description": g.description,
                    "severity": g.severity,
                    "file": str(g.file) if g.file else None,
                }
                for g in recommendations.gaps
            ],
            "next_steps": [
                {
                    "priority": s.priority,
                    "order": s.order,
                    "action": s.action,
                    "rationale": s.rationale,
                    "impact": s.impact,
                    "effort": s.effort,
                }
                for s in recommendations.next_steps
            ],
        }
        
        if verbose:
            output["statistics"] = {
                "code": {
                    "files": code_analysis.file_count,
                    "lines": code_analysis.line_count,
                    "python_files": code_analysis.python_files,
                    "javascript_files": code_analysis.javascript_files,
                    "todos": len(code_analysis.todos),
                    "fixmes": len(code_analysis.fixmes),
                },
                "tests": {
                    "coverage": test_analysis.coverage_percentage,
                    "test_files": test_analysis.test_count,
                    "untested_files": len(test_analysis.untested_files),
                },
                "git": {
                    "commits_7d": git_analysis.commit_count_7d,
                    "commits_30d": git_analysis.commit_count_30d,
                    "commits_per_day": git_analysis.commits_per_day,
                    "contributors": git_analysis.contributors,
                    "last_commit": git_analysis.last_commit_date.isoformat() if git_analysis.last_commit_date else None,
                } if git_analysis.is_git_repo else None,
            }
        
        return json.dumps(output, indent=2)


def save_report(
    content: str,
    format: str,
    output_path: Optional[Path] = None,
) -> Path:
    """Save report to file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = "md" if format == "markdown" else "json"
        output_path = Path.cwd() / f"nextstep_report_{timestamp}.{ext}"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    return output_path
