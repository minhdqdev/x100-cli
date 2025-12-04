"""User story analyzer for tracking implementation status."""

import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class UserStoryStatus:
    """Status of a user story."""
    
    id: str
    title: str
    status: str  # 'todo', 'in-progress', 'done', 'unknown'
    file_path: Path
    has_implementation: bool = False
    has_tests: bool = False
    acceptance_criteria_count: int = 0
    completion_percentage: int = 0


class StoryAnalyzer:
    """Analyze user stories and their implementation status."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.stories_path = project_path / "docs" / "user-stories"
    
    def analyze(self) -> List[UserStoryStatus]:
        """Analyze all user stories."""
        if not self.stories_path.exists():
            return []
        
        stories = []
        for story_file in self.stories_path.glob("US-*.md"):
            story = self._analyze_story(story_file)
            if story:
                stories.append(story)
        
        return stories
    
    def _analyze_story(self, story_file: Path) -> Optional[UserStoryStatus]:
        """Analyze a single user story file."""
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract story ID and title
            story_id = story_file.stem
            title = self._extract_title(content)
            
            # Determine status
            status = self._extract_status(content)
            
            # Count acceptance criteria
            ac_count = self._count_acceptance_criteria(content)
            
            # Check for implementation references
            has_impl = self._has_implementation_reference(content)
            
            # Check for test references
            has_tests = self._has_test_reference(content)
            
            # Calculate completion percentage
            completion = self._calculate_completion(status, has_impl, has_tests)
            
            return UserStoryStatus(
                id=story_id,
                title=title,
                status=status,
                file_path=story_file.relative_to(self.project_path),
                has_implementation=has_impl,
                has_tests=has_tests,
                acceptance_criteria_count=ac_count,
                completion_percentage=completion,
            )
        except Exception:
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extract title from user story."""
        # Look for markdown h1 or h2
        title_match = re.search(r'^#{1,2}\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        return "Untitled"
    
    def _extract_status(self, content: str) -> str:
        """Extract status from user story."""
        content_lower = content.lower()
        
        # Look for explicit status markers
        if 'status: done' in content_lower or 'status: completed' in content_lower or '✅' in content:
            return 'done'
        elif 'status: in progress' in content_lower or 'status: in-progress' in content_lower:
            return 'in-progress'
        elif 'status: todo' in content_lower or 'status: not started' in content_lower:
            return 'todo'
        
        # Check checkbox-based completion in acceptance criteria
        ac_section = re.search(
            r'#+\s*Acceptance Criteria.*?(?=\n#+|\Z)',
            content,
            re.IGNORECASE | re.DOTALL
        )
        
        if ac_section:
            section_text = ac_section.group(0)
            # Count checked and unchecked checkboxes
            checked = len(re.findall(r'- \[x\]', section_text, re.IGNORECASE))
            unchecked = len(re.findall(r'- \[ \]', section_text))
            total = checked + unchecked
            
            if total > 0:
                completion_ratio = checked / total
                if completion_ratio == 1.0:
                    return 'done'
                elif completion_ratio > 0.0:
                    return 'in-progress'
                else:
                    return 'todo'
        
        # Fallback: infer from keywords (but avoid false positives from checkbox text)
        # Only check in non-checkbox contexts
        lines_without_checkboxes = [
            line for line in content.split('\n')
            if not re.match(r'^\s*[-*]\s+\[[ xX]\]', line)
        ]
        clean_content = '\n'.join(lines_without_checkboxes).lower()
        
        if 'implemented and deployed' in clean_content or 'implementation complete' in clean_content:
            return 'done'
        elif 'working on' in clean_content or 'currently implementing' in clean_content:
            return 'in-progress'
        
        return 'todo'  # Default to 'todo' rather than 'unknown'
    
    def _count_acceptance_criteria(self, content: str) -> int:
        """Count acceptance criteria in story."""
        # Look for bullet points under "Acceptance Criteria" section
        ac_section = re.search(
            r'#+\s*Acceptance Criteria.*?(?=\n#+|\Z)',
            content,
            re.IGNORECASE | re.DOTALL
        )
        
        if ac_section:
            section_text = ac_section.group(0)
            # Count bullet points
            bullets = re.findall(r'^\s*[-*]\s+', section_text, re.MULTILINE)
            return len(bullets)
        
        return 0
    
    def _has_implementation_reference(self, content: str) -> bool:
        """Check if story references implementation files."""
        # Look for code file references
        code_patterns = [
            r'`[\w/]+\.py`',
            r'`[\w/]+\.js`',
            r'`[\w/]+\.ts`',
            r'implemented in',
            r'code in',
            r'file:.*\.py',
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _has_test_reference(self, content: str) -> bool:
        """Check if story references tests."""
        # Look for test references
        test_patterns = [
            r'test[_\s]',
            r'spec[_\s]',
            r'`test_[\w]+\.py`',
            r'`[\w]+\.test\.js`',
        ]
        
        for pattern in test_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _calculate_completion(
        self,
        status: str,
        has_impl: bool,
        has_tests: bool
    ) -> int:
        """Calculate completion percentage."""
        if status == 'done':
            return 100
        elif status == 'todo':
            return 0
        
        score = 0
        
        # Status contributes 50%
        if status == 'in-progress':
            score += 50
        
        # Implementation contributes 30%
        if has_impl:
            score += 30
        
        # Tests contribute 20%
        if has_tests:
            score += 20
        
        return min(score, 100)
    
    def get_incomplete_stories(self) -> List[UserStoryStatus]:
        """Get stories that are not completed."""
        stories = self.analyze()
        return [s for s in stories if s.status != 'done']
    
    def get_stories_without_implementation(self) -> List[UserStoryStatus]:
        """Get stories marked done but without implementation reference."""
        stories = self.analyze()
        return [
            s for s in stories
            if s.status == 'done' and not s.has_implementation
        ]
    
    def get_stories_without_tests(self) -> List[UserStoryStatus]:
        """Get stories without test references."""
        stories = self.analyze()
        return [s for s in stories if not s.has_tests and s.status != 'todo']
