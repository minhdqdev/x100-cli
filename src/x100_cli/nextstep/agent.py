"""AI agent integration for nextstep analysis."""

from datetime import datetime
from typing import Optional
import re

from .models import (
    CodeAnalysis,
    GitAnalysis,
    TestAnalysis,
    ProjectStatus,
    Recommendations,
    HealthScore,
    Blocker,
    Gap,
    NextStep,
)


class NextStepAgent:
    """AI agent for analyzing project and generating recommendations."""
    
    def __init__(self):
        pass
    
    def analyze_and_recommend(
        self,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
        project_status: Optional[ProjectStatus] = None,
    ) -> Recommendations:
        """Analyze project data and generate recommendations."""
        
        # Calculate health score
        health_score = self._calculate_health_score(
            code_analysis,
            git_analysis,
            test_analysis,
        )
        
        # Identify blockers
        blockers = self._identify_blockers(
            code_analysis,
            git_analysis,
            test_analysis,
            project_status,
        )
        
        # Find gaps
        gaps = self._find_gaps(
            code_analysis,
            test_analysis,
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(
            code_analysis,
            git_analysis,
            test_analysis,
            blockers,
            gaps,
        )
        
        return Recommendations(
            health_score=health_score,
            blockers=blockers,
            gaps=gaps,
            next_steps=next_steps,
        )
    
    def _calculate_health_score(
        self,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
    ) -> HealthScore:
        """Calculate overall project health score."""
        
        # Activity score (0-100) based on git activity
        if git_analysis.is_git_repo:
            if git_analysis.commits_per_day >= 2.0:
                activity_score = 100
            elif git_analysis.commits_per_day >= 1.0:
                activity_score = 80
            elif git_analysis.commits_per_day >= 0.5:
                activity_score = 60
            elif git_analysis.commit_count_7d > 0:
                activity_score = 40
            else:
                activity_score = 20
        else:
            activity_score = 50  # Not a git repo, neutral score
        
        # Quality score (0-100) based on test coverage and markers
        quality_score = 100
        if test_analysis.coverage_percentage is not None:
            coverage_penalty = max(0, 80 - test_analysis.coverage_percentage)
            quality_score -= coverage_penalty
        
        # Penalty for TODOs and FIXMEs
        marker_count = len(code_analysis.todos) + len(code_analysis.fixmes)
        if marker_count > 50:
            quality_score -= 20
        elif marker_count > 20:
            quality_score -= 10
        elif marker_count > 10:
            quality_score -= 5
        
        quality_score = max(0, quality_score)
        
        # Blocker score (0-100) - higher is better (fewer blockers)
        blocker_score = 100
        fixme_count = len(code_analysis.fixmes)
        if fixme_count > 20:
            blocker_score = 40
        elif fixme_count > 10:
            blocker_score = 60
        elif fixme_count > 5:
            blocker_score = 80
        
        # Velocity score (0-100) based on recent activity
        if git_analysis.is_git_repo:
            if git_analysis.commit_count_7d >= 14:  # 2+ commits per day
                velocity_score = 100
            elif git_analysis.commit_count_7d >= 7:  # 1 per day
                velocity_score = 85
            elif git_analysis.commit_count_7d >= 3:
                velocity_score = 70
            elif git_analysis.commit_count_7d > 0:
                velocity_score = 50
            else:
                velocity_score = 30
        else:
            velocity_score = 50
        
        # Calculate overall score (weighted average)
        overall = int(
            velocity_score * 0.2 +
            quality_score * 0.3 +
            blocker_score * 0.3 +
            activity_score * 0.2
        )
        
        # Determine summary and trend
        if overall >= 80:
            summary = "Excellent"
            trend = "improving"
        elif overall >= 70:
            summary = "Good"
            trend = "stable"
        elif overall >= 60:
            summary = "Fair"
            trend = "stable"
        elif overall >= 50:
            summary = "Needs Attention"
            trend = "declining"
        else:
            summary = "Poor"
            trend = "declining"
        
        return HealthScore(
            overall=overall,
            velocity_score=velocity_score,
            quality_score=quality_score,
            blocker_score=blocker_score,
            activity_score=activity_score,
            summary=summary,
            trend=trend,
        )
    
    def _identify_blockers(
        self,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
        project_status: Optional[ProjectStatus],
    ) -> list[Blocker]:
        """Identify blocking issues."""
        blockers = []
        
        # FIXMEs are potential blockers
        if len(code_analysis.fixmes) > 5:
            blockers.append(Blocker(
                title=f"{len(code_analysis.fixmes)} FIXME markers in codebase",
                impact="Technical debt accumulating",
                source="code",
                details=f"Found {len(code_analysis.fixmes)} FIXME markers that need attention",
            ))
        
        # Low test coverage is a blocker
        if test_analysis.coverage_percentage is not None and test_analysis.coverage_percentage < 60:
            blockers.append(Blocker(
                title=f"Low test coverage ({test_analysis.coverage_percentage}%)",
                impact="High risk of production issues",
                source="code",
                details=f"Coverage is {test_analysis.coverage_percentage}%, target should be >80%",
            ))
        
        # Stale repository
        if git_analysis.is_git_repo and git_analysis.commit_count_7d == 0:
            blockers.append(Blocker(
                title="No recent commits (7+ days)",
                impact="Project appears inactive",
                source="git",
                details="No commits in the last 7 days may indicate stalled development",
            ))
        
        # GitHub blockers
        if project_status and project_status.blocked_issues:
            for issue in project_status.blocked_issues:
                blockers.append(Blocker(
                    title=f"Issue #{issue.number}: {issue.title}",
                    impact=f"Blocked for {issue.created_days_ago} days",
                    source="github",
                    details="Blocking other work",
                ))
        
        return blockers
    
    def _find_gaps(
        self,
        code_analysis: CodeAnalysis,
        test_analysis: TestAnalysis,
    ) -> list[Gap]:
        """Find gaps and inconsistencies."""
        gaps = []
        
        # Untested files
        if test_analysis.untested_files:
            high_risk_files = [
                f for f in test_analysis.untested_files
                if any(keyword in str(f).lower() for keyword in ['payment', 'auth', 'security', 'api'])
            ]
            
            if high_risk_files:
                for file in high_risk_files[:3]:  # Top 3
                    gaps.append(Gap(
                        category="Quality Gap",
                        description=f"{file.name}: No tests (high risk module)",
                        severity="high",
                        file=file,
                    ))
            elif len(test_analysis.untested_files) > 5:
                gaps.append(Gap(
                    category="Quality Gap",
                    description=f"{len(test_analysis.untested_files)} files without tests",
                    severity="medium",
                ))
        
        # Old TODOs
        old_todos = [t for t in code_analysis.todos if t.age_days and t.age_days > 30]
        if len(old_todos) > 10:
            gaps.append(Gap(
                category="Technical Debt",
                description=f"{len(old_todos)} TODO markers older than 30 days",
                severity="medium",
            ))
        
        return gaps
    
    def _generate_next_steps(
        self,
        code_analysis: CodeAnalysis,
        git_analysis: GitAnalysis,
        test_analysis: TestAnalysis,
        blockers: list[Blocker],
        gaps: list[Gap],
    ) -> list[NextStep]:
        """Generate prioritized next steps."""
        steps = []
        order = 1
        
        # Address critical blockers first (NOW priority)
        if test_analysis.coverage_percentage is not None and test_analysis.coverage_percentage < 60:
            steps.append(NextStep(
                priority="NOW",
                action="Increase test coverage to >60%",
                rationale="Current coverage is critically low, high risk of production issues",
                impact="Reduces risk, improves confidence in changes",
                effort="4-8 hours",
                order=order,
            ))
            order += 1
        
        # Address high-risk untested files
        high_risk_untested = [
            f for f in test_analysis.untested_files
            if any(keyword in str(f).lower() for keyword in ['payment', 'auth', 'security'])
        ]
        if high_risk_untested:
            file = high_risk_untested[0]
            steps.append(NextStep(
                priority="NOW",
                action=f"Add tests for {file.name}",
                rationale="High-risk module without test coverage",
                impact="Reduces production risk for critical functionality",
                effort="2-4 hours",
                order=order,
            ))
            order += 1
        
        # Address FIXMEs (This Week priority)
        if len(code_analysis.fixmes) > 5:
            steps.append(NextStep(
                priority="This Week",
                action=f"Address {len(code_analysis.fixmes)} FIXME markers",
                rationale="Technical debt is accumulating",
                impact="Improves code quality and maintainability",
                effort="4-8 hours",
                order=order,
            ))
            order += 1
        
        # General improvements
        if len(code_analysis.todos) > 20:
            steps.append(NextStep(
                priority="This Week",
                action=f"Review and clean up {len(code_analysis.todos)} TODO markers",
                rationale="Keep technical debt under control",
                impact="Clarifies remaining work, prevents debt accumulation",
                effort="2-4 hours",
                order=order,
            ))
            order += 1
        
        # Velocity improvements
        if git_analysis.is_git_repo and git_analysis.commits_per_day < 1.0:
            steps.append(NextStep(
                priority="Next Sprint",
                action="Increase development velocity",
                rationale="Current velocity is below optimal",
                impact="Faster feature delivery",
                effort="Planning session",
                order=order,
            ))
            order += 1
        
        # If no specific issues, suggest general improvements
        if not steps:
            steps.append(NextStep(
                priority="Next Sprint",
                action="Continue current trajectory",
                rationale="Project health is good, maintain momentum",
                impact="Sustained quality and delivery",
                effort="Ongoing",
                order=order,
            ))
        
        return steps
