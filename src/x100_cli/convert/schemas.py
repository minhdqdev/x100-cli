"""Schema definitions for user story to GitHub issue conversion."""

import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, asdict


# Load the JSON schema
SCHEMA_PATH = Path(__file__).parent / "github_issue_schema.json"
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    GITHUB_ISSUE_JSON_SCHEMA = json.load(f)


@dataclass
class GitHubIssueSchema:
    """Data class representing a GitHub issue."""

    title: str
    body: str
    labels: Optional[List[str]] = None
    issue_type: Optional[str] = "Task"
    assignees: Optional[List[str]] = None
    milestone: Optional[int] = None
    project_id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary, filtering out None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "GitHubIssueSchema":
        """Create instance from dictionary."""
        return cls(
            title=data["title"],
            body=data["body"],
            labels=data.get("labels"),
            issue_type=data.get("issue_type", "Task"),
            assignees=data.get("assignees"),
            milestone=data.get("milestone"),
            project_id=data.get("project_id"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "GitHubIssueSchema":
        """Create instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def get_json_schema(cls) -> dict:
        """Get the JSON schema for validation."""
        return GITHUB_ISSUE_JSON_SCHEMA


def get_schema_prompt() -> str:
    """
    Get a prompt text to include in AI agent instructions for issue conversion.

    Returns:
        A formatted string with schema instructions.
    """
    schema_json = json.dumps(GITHUB_ISSUE_JSON_SCHEMA, indent=2)

    return f"""
You must convert the user story to a JSON object that strictly follows this schema:

{schema_json}

IMPORTANT INSTRUCTIONS:
1. The output MUST be valid JSON only - no markdown code blocks, no explanations
2. Extract the title from the user story heading or filename
3. Convert the entire user story content to markdown format for the body field
4. Infer appropriate labels from the user story content (e.g., "feature", "bug", "enhancement", "backend", "frontend")
5. Do not include assignees unless explicitly specified in the user story
6. Do not include milestone unless explicitly specified
7. Do not include project_id - it will be added automatically if configured

OUTPUT FORMAT:
Return ONLY the JSON object. Do not wrap it in code blocks or add any explanatory text.

Example output:
{{
  "title": "Implement user authentication",
  "body": "## User Story\\n\\nAs a user...\\n\\n## Acceptance Criteria\\n\\n- [ ] ...",
  "labels": ["feature", "security", "backend"]
}}
"""
