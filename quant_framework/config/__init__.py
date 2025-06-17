"""
Configuration management for the quantitative finance framework.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

class Config:
    """Configuration manager for the framework."""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file and environment variables."""
        # Load environment variables
        load_dotenv()
        
        # Load YAML configuration
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)
        
        # Replace environment variables
        self._replace_env_vars(self._config)
    
    def _replace_env_vars(self, config: Dict[str, Any]):
        """Replace ${VAR} with environment variable values."""
        for key, value in config.items():
            if isinstance(value, dict):
                self._replace_env_vars(value)
            elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key."""
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """Save current configuration to YAML file."""
        if path is None:
            path = Path(__file__).parent / "config.yaml"
        
        with open(path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self._config.copy() 