"""Test analyzer for test coverage analysis."""

from pathlib import Path
from typing import List

from ..models import TestAnalysis


class TestAnalyzer:
    """Analyze test coverage and quality."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.test_patterns = [
            '**/test_*.py',
            '**/*_test.py',
            '**/tests/**/*.py',
            '**/*.test.js',
            '**/*.test.ts',
            '**/*.test.tsx',
            '**/*.spec.js',
            '**/*.spec.ts',
            '**/*.spec.tsx',
        ]
    
    def analyze(self) -> TestAnalysis:
        """Perform complete test analysis."""
        test_files = self._find_test_files()
        test_count = len(test_files)
        
        # Try to get coverage from .coverage file or coverage.xml
        coverage = self._get_coverage_percentage()
        
        # Find untested Python files
        untested_files = self._find_untested_files()
        
        return TestAnalysis(
            coverage_percentage=coverage,
            test_count=test_count,
            untested_files=untested_files,
            test_files=test_files,
        )
    
    def _find_test_files(self) -> List[Path]:
        """Find all test files."""
        test_files = []
        for pattern in self.test_patterns:
            for file in self.project_path.glob(pattern):
                if file.is_file():
                    # Exclude files in common exclude dirs
                    if any(p in str(file) for p in ['.venv', 'venv', 'node_modules', '.tox']):
                        continue
                    test_files.append(file.relative_to(self.project_path))
        return test_files
    
    def _get_coverage_percentage(self) -> float | None:
        """Try to extract coverage percentage."""
        # Try coverage.xml first (common in Python projects)
        coverage_xml = self.project_path / "coverage.xml"
        if coverage_xml.exists():
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(coverage_xml)
                root = tree.getroot()
                # Look for line-rate attribute
                line_rate = root.attrib.get('line-rate')
                if line_rate:
                    return round(float(line_rate) * 100, 1)
            except Exception:
                pass
        
        # Try .coverage file (SQLite database used by coverage.py)
        coverage_file = self.project_path / ".coverage"
        if coverage_file.exists():
            try:
                import sqlite3
                conn = sqlite3.connect(coverage_file)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT SUM(numbits) as total_lines,
                           SUM(numbits - (length(replace(hex(bitmap), '0', '')))) as covered_lines
                    FROM line_bits
                ''')
                result = cursor.fetchone()
                if result and result[0]:
                    total, covered = result
                    if total > 0:
                        return round((covered / total) * 100, 1)
            except Exception:
                pass
        
        return None
    
    def _find_untested_files(self) -> List[Path]:
        """Find Python source files without corresponding tests."""
        untested = []
        
        # Find all Python source files (excluding tests)
        for py_file in self.project_path.rglob('*.py'):
            if py_file.is_file():
                # Skip if in excluded dirs
                if any(p in str(py_file) for p in ['.venv', 'venv', 'node_modules', '.tox', '__pycache__']):
                    continue
                
                # Skip if it's a test file
                if any(pattern in str(py_file) for pattern in ['test_', '_test.py', '/tests/']):
                    continue
                
                # Skip __init__.py files
                if py_file.name == '__init__.py':
                    continue
                
                # Check if corresponding test exists
                if not self._has_test_file(py_file):
                    untested.append(py_file.relative_to(self.project_path))
        
        return untested
    
    def _has_test_file(self, source_file: Path) -> bool:
        """Check if a source file has a corresponding test file."""
        # Try common test file naming patterns
        parent = source_file.parent
        stem = source_file.stem
        
        test_candidates = [
            parent / f"test_{stem}.py",
            parent / f"{stem}_test.py",
            parent / "tests" / f"test_{stem}.py",
            parent.parent / "tests" / parent.name / f"test_{stem}.py",
        ]
        
        return any(candidate.exists() for candidate in test_candidates)
