"""Configuration management for nextstep."""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class AnalysisConfig:
    """Configuration for analysis thresholds."""
    
    coverage_threshold: int = 80
    stale_issue_days: int = 30
    stale_pr_days: int = 7
    old_todo_days: int = 30
    max_fixme_count: int = 10


@dataclass
class GitHubConfig:
    """GitHub integration configuration."""
    
    enabled: bool = False
    token_env: str = "GITHUB_TOKEN"
    repo: Optional[str] = None
    project_number: Optional[int] = None


@dataclass
class HealthWeights:
    """Weights for health score calculation."""
    
    velocity: float = 0.2
    quality: float = 0.3
    blockers: float = 0.3
    activity: float = 0.2


@dataclass
class NextStepConfig:
    """Complete nextstep configuration."""
    
    default_ai_agent: str = "claude"
    analysis: AnalysisConfig = None
    github: GitHubConfig = None
    health_weights: HealthWeights = None
    
    def __post_init__(self):
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.github is None:
            self.github = GitHubConfig()
        if self.health_weights is None:
            self.health_weights = HealthWeights()


def load_config(config_path: Optional[Path] = None) -> NextStepConfig:
    """Load configuration from file or use defaults."""
    if config_path is None:
        config_path = Path.cwd() / ".x100" / "nextstep.json"
    
    # Try to read default agent from main config
    default_agent = "claude"
    main_config_path = Path.cwd() / ".x100" / "config.json"
    if main_config_path.exists():
        try:
            import json
            main_config = json.loads(main_config_path.read_text(encoding="utf-8"))
            default_agent = main_config.get("default_agent", "claude")
        except Exception:
            pass
    
    if not config_path.exists():
        return NextStepConfig(default_ai_agent=default_agent)
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        config = NextStepConfig(
            default_ai_agent=data.get("default_ai_agent", default_agent),
        )
        
        if "analysis" in data:
            config.analysis = AnalysisConfig(**data["analysis"])
        
        if "github" in data:
            config.github = GitHubConfig(**data["github"])
        
        if "health_weights" in data:
            config.health_weights = HealthWeights(**data["health_weights"])
        
        return config
    except Exception:
        # If config is invalid, return defaults
        return NextStepConfig()


def save_config(config: NextStepConfig, config_path: Optional[Path] = None):
    """Save configuration to file."""
    if config_path is None:
        config_path = Path.cwd() / ".x100" / "nextstep.json"
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "default_ai_agent": config.default_ai_agent,
        "analysis": asdict(config.analysis),
        "github": asdict(config.github),
        "health_weights": asdict(config.health_weights),
    }
    
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)


def create_default_config(output_path: Optional[Path] = None) -> Path:
    """Create a default configuration file."""
    if output_path is None:
        output_path = Path.cwd() / ".x100" / "nextstep.json"
    
    config = NextStepConfig()
    save_config(config, output_path)
    return output_path
