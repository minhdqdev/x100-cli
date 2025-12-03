"""Documentation analyzer for coverage analysis."""

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class DocumentationStatus:
    """Documentation status of the project."""
    
    has_readme: bool = False
    has_changelog: bool = False
    has_contributing: bool = False
    has_license: bool = False
    has_prd: bool = False
    has_architecture: bool = False
    docs_folder_exists: bool = False
    doc_file_count: int = 0
    readme_lines: int = 0
    outdated_docs: List[Path] = None
    
    def __post_init__(self):
        if self.outdated_docs is None:
            self.outdated_docs = []


class DocsAnalyzer:
    """Analyze project documentation coverage."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.docs_path = project_path / "docs"
    
    def analyze(self) -> DocumentationStatus:
        """Perform complete documentation analysis."""
        status = DocumentationStatus()
        
        # Check for key documentation files
        status.has_readme = (self.project_path / "README.md").exists()
        status.has_changelog = (self.project_path / "CHANGELOG.md").exists()
        status.has_contributing = (self.project_path / "CONTRIBUTING.md").exists()
        status.has_license = self._check_license_exists()
        
        # Check docs folder
        status.docs_folder_exists = self.docs_path.exists()
        
        if status.docs_folder_exists:
            # Check for key docs
            status.has_prd = (self.docs_path / "PRD.md").exists()
            status.has_architecture = self._check_architecture_docs()
            
            # Count doc files
            status.doc_file_count = len(list(self.docs_path.rglob("*.md")))
        
        # Check README size
        if status.has_readme:
            readme_path = self.project_path / "README.md"
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    status.readme_lines = len(f.readlines())
            except Exception:
                pass
        
        # Find potentially outdated docs
        status.outdated_docs = self._find_outdated_docs()
        
        return status
    
    def _check_license_exists(self) -> bool:
        """Check if license file exists."""
        license_files = [
            "LICENSE",
            "LICENSE.md",
            "LICENSE.txt",
            "COPYING",
        ]
        
        for license_file in license_files:
            if (self.project_path / license_file).exists():
                return True
        
        return False
    
    def _check_architecture_docs(self) -> bool:
        """Check for architecture documentation."""
        arch_files = [
            "ARCHITECTURE.md",
            "architecture.md",
            "DESIGN.md",
            "design.md",
        ]
        
        for arch_file in arch_files:
            if (self.docs_path / arch_file).exists():
                return True
            if (self.project_path / arch_file).exists():
                return True
        
        return False
    
    def _find_outdated_docs(self) -> List[Path]:
        """Find documentation files that might be outdated."""
        # This is a simple heuristic - could be enhanced with git timestamps
        outdated = []
        
        if not self.docs_path.exists():
            return outdated
        
        for doc_file in self.docs_path.rglob("*.md"):
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Look for TODO or FIXME markers in docs
                if 'todo' in content or 'fixme' in content or 'tbd' in content:
                    outdated.append(doc_file.relative_to(self.project_path))
            except Exception:
                continue
        
        return outdated
    
    def calculate_coverage_score(self) -> int:
        """Calculate documentation coverage score (0-100)."""
        status = self.analyze()
        score = 0
        
        # Essential docs (60 points)
        if status.has_readme:
            score += 20
            # Bonus for substantial README
            if status.readme_lines >= 50:
                score += 10
        
        if status.has_license:
            score += 10
        
        if status.has_changelog:
            score += 10
        
        if status.has_contributing:
            score += 10
        
        # Project docs (30 points)
        if status.docs_folder_exists:
            score += 10
        
        if status.has_prd:
            score += 10
        
        if status.has_architecture:
            score += 10
        
        # Quality bonus (10 points)
        if status.doc_file_count >= 5:
            score += 5
        
        if len(status.outdated_docs) == 0:
            score += 5
        
        return min(score, 100)
    
    def get_missing_docs(self) -> List[str]:
        """Get list of missing documentation."""
        status = self.analyze()
        missing = []
        
        if not status.has_readme:
            missing.append("README.md")
        
        if not status.has_license:
            missing.append("LICENSE")
        
        if not status.has_changelog:
            missing.append("CHANGELOG.md")
        
        if not status.has_contributing:
            missing.append("CONTRIBUTING.md")
        
        if not status.has_prd:
            missing.append("docs/PRD.md")
        
        if not status.has_architecture:
            missing.append("docs/ARCHITECTURE.md")
        
        return missing
