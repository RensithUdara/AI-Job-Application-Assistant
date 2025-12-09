"""
Configuration loader utility.
Loads all JSON configuration files and provides easy access to config values.
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path

class ConfigLoader:
    """Load and manage all application configurations from JSON files."""
    
    _instance = None
    _configs = {}
    
    def __new__(cls):
        """Implement singleton pattern for config loader."""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize and load all configuration files."""
        config_dir = Path(__file__).parent.parent / 'data'
        config_files = [
            'app_config.json',
            'career_paths.json',
            'role_config.json',
            'resume_config.json',
            'mock_interview_questions.json',
            'learning_resources.json',
            'ui_elements.json'
        ]
        
        for config_file in config_files:
            try:
                file_path = config_dir / config_file
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        self._configs[config_file] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {config_file}: {e}")
    
    def get_config(self, config_name: str, key: str = None, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            config_name: Name of config file (e.g., 'app_config.json')
            key: Optional dot-notation path to nested value (e.g., 'ui_config.priority_icons.high')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        if config_name not in self._configs:
            return default
        
        config = self._configs[config_name]
        
        if key is None:
            return config
        
        # Support dot notation for nested keys
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_app_config(self, key: str = None, default: Any = None) -> Any:
        """Get app configuration."""
        return self.get_config('app_config.json', key, default)
    
    def get_career_paths(self, key: str = None, default: Any = None) -> Any:
        """Get career paths configuration."""
        return self.get_config('career_paths.json', key, default)
    
    def get_role_config(self, key: str = None, default: Any = None) -> Any:
        """Get role configuration."""
        return self.get_config('role_config.json', key, default)
    
    def get_resume_config(self, key: str = None, default: Any = None) -> Any:
        """Get resume configuration."""
        return self.get_config('resume_config.json', key, default)
    
    def get_interview_questions(self, key: str = None, default: Any = None) -> Any:
        """Get interview questions configuration."""
        return self.get_config('mock_interview_questions.json', key, default)
    
    def reload_config(self, config_name: str = None):
        """Reload configuration from file."""
        if config_name:
            # Reload specific config
            self._configs = {}
            self._initialize()
        else:
            # Reload all configs
            self._initialize()


# Global config loader instance
config = ConfigLoader()


# Convenience functions for commonly accessed configs
def get_ui_config(key: str = None, default: Any = None) -> Any:
    """Get UI configuration."""
    return config.get_config('app_config.json', f'ui_config.{key}' if key else 'ui_config', default)


def get_priority_icon(priority: str) -> str:
    """Get priority icon based on priority level."""
    icons = config.get_config('app_config.json', 'ui_config.priority_icons', {})
    return icons.get(priority.lower(), '⚪')


def get_match_score_icon(score: float) -> str:
    """Get match score icon based on score value."""
    colors = config.get_config('app_config.json', 'ui_config.match_score_colors', {})
    
    if score >= 80:
        return colors.get('excellent', '🟢')
    elif score >= 60:
        return colors.get('good', '🟡')
    elif score >= 40:
        return colors.get('fair', '🟠')
    else:
        return colors.get('poor', '🔴')


def get_strong_action_verbs() -> List[str]:
    """Get list of strong action verbs."""
    return config.get_config('resume_config.json', 'action_verbs.strong', [])


def get_weak_action_verbs() -> List[str]:
    """Get list of weak action verbs."""
    return config.get_config('resume_config.json', 'action_verbs.weak', [])


def get_role_keywords(role: str) -> List[str]:
    """Get keywords for a specific role."""
    keywords = config.get_config('role_config.json', 'role_keywords', {})
    return keywords.get(role, [])


def get_role_required_skills(role: str) -> List[str]:
    """Get required skills for a specific role."""
    skills = config.get_config('role_config.json', 'role_required_skills', {})
    return skills.get(role, [])


def get_career_roadmap(role: str, level: str = 'beginner') -> List[Dict]:
    """Get career roadmap for a specific role and level."""
    roadmaps = config.get_config('career_paths.json', 'career_roadmaps', {})
    return roadmaps.get(role, {}).get(level, [])


def get_interview_questions_by_type(question_type: str, difficulty: str = 'Medium') -> List[str]:
    """Get interview questions by type and difficulty."""
    questions = config.get_config('mock_interview_questions.json', f'{question_type}.{difficulty}', [])
    return questions if isinstance(questions, list) else []
