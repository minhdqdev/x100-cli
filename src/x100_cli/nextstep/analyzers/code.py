"""Code analyzer for codebase health analysis."""

import re
from pathlib import Path
from typing import List
from datetime import datetime

from ..models import CodeAnalysis, TodoItem


class CodeAnalyzer:
    """Analyze codebase structure and health."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.exclude_dirs = {
            '.git', '.venv', 'venv', 'node_modules', '__pycache__',
            '.pytest_cache', '.mypy_cache', 'dist', 'build', '.next',
            'coverage', '.coverage', '.tox', 'htmlcov'
        }
        self.code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java',
            '.rs', '.rb', '.php', '.c', '.cpp', '.h', '.hpp'
        }
    
    def analyze(self) -> CodeAnalysis:
        """Perform complete code analysis."""
        files = self._get_code_files()
        
        file_count = len(files)
        line_count = self._count_lines(files)
        python_files = len([f for f in files if f.suffix == '.py'])
        javascript_files = len([f for f in files if f.suffix in {'.js', '.jsx', '.ts', '.tsx'}])
        other_files = file_count - python_files - javascript_files
        
        todos, fixmes = self._find_markers(files)
        
        return CodeAnalysis(
            file_count=file_count,
            line_count=line_count,
            python_files=python_files,
            javascript_files=javascript_files,
            other_files=other_files,
            todos=todos,
            fixmes=fixmes,
        )
    
    def _get_code_files(self) -> List[Path]:
        """Get all code files, excluding specified directories."""
        files = []
        for path in self.project_path.rglob('*'):
            if path.is_file():
                # Check if any parent directory is in exclude list
                if any(parent.name in self.exclude_dirs for parent in path.parents):
                    continue
                if path.suffix in self.code_extensions:
                    files.append(path)
        return files
    
    def _count_lines(self, files: List[Path]) -> int:
        """Count total lines of code."""
        total = 0
        for file in files:
            try:
                with file.open('r', encoding='utf-8', errors='ignore') as f:
                    total += sum(1 for _ in f)
            except Exception:
                continue
        return total
    
    def _find_markers(self, files: List[Path]) -> tuple[List[TodoItem], List[TodoItem]]:
        """Find TODO and FIXME markers in code."""
        todo_pattern = re.compile(r'#\s*TODO:?\s*(.+)|//\s*TODO:?\s*(.+)', re.IGNORECASE)
        fixme_pattern = re.compile(r'#\s*FIXME:?\s*(.+)|//\s*FIXME:?\s*(.+)', re.IGNORECASE)
        
        todos = []
        fixmes = []
        
        for file in files:
            try:
                with file.open('r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        # Check for TODO
                        todo_match = todo_pattern.search(line)
                        if todo_match:
                            text = (todo_match.group(1) or todo_match.group(2) or '').strip()
                            todos.append(TodoItem(
                                file=file.relative_to(self.project_path),
                                line=line_num,
                                text=text,
                                type='TODO'
                            ))
                        
                        # Check for FIXME
                        fixme_match = fixme_pattern.search(line)
                        if fixme_match:
                            text = (fixme_match.group(1) or fixme_match.group(2) or '').strip()
                            fixmes.append(TodoItem(
                                file=file.relative_to(self.project_path),
                                line=line_num,
                                text=text,
                                type='FIXME'
                            ))
            except Exception:
                continue
        
        return todos, fixmes
    
    def find_user_stories(self) -> List[Path]:
        """Find user story files."""
        stories_path = self.project_path / "docs" / "user-stories"
        if not stories_path.exists():
            return []
        
        return list(stories_path.glob("US-*.md"))
