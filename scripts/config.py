#!/usr/bin/env python3
"""
Configuration Management Module.

This module provides configuration management functionality for the
Knowledge Assistant system, including YAML configuration loading,
validation, and access.

Example:
    >>> from scripts.config import ConfigManager
    >>> config = ConfigManager('config.yaml')
    >>> config.load()
    >>> value = config.get('template_dir', default='./templates')
"""

from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigurationError(Exception):
    """Exception raised for configuration-related errors."""

    pass


class ConfigManager:
    """
    Configuration manager for loading and managing YAML configuration files.

    This class provides functionality to load YAML configuration files,
    validate them, and access configuration values.

    Attributes:
        config_path (Path): Path to the configuration file.
        config (Dict[str, Any]): The loaded configuration data.

    Example:
        >>> config = ConfigManager('config.yaml')
        >>> config.load()
        >>> template_dir = config.get('template_dir')
        >>> print(template_dir)
        './templates'
    """

    # Default configuration values
    DEFAULT_CONFIG: Dict[str, Any] = {
        "template_dir": "./templates",
        "output_dir": "./output",
        "default_author": "Knowledge Assistant",
        "date_format": "%Y-%m-%d",
        "templates": {
            "daily-note": {
                "enabled": True,
                "auto_date": True,
            },
            "research-note": {
                "enabled": True,
            },
            "meeting-minutes": {
                "enabled": True,
            },
            "task-list": {
                "enabled": True,
            },
            "knowledge-card": {
                "enabled": True,
            },
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file. If None, uses
                        default configuration only.

        Example:
            >>> config = ConfigManager('config.yaml')
            >>> config = ConfigManager()  # Uses defaults only
        """
        self.config_path = Path(config_path) if config_path else None
        self.config: Dict[str, Any] = {}

    def load(self, use_defaults: bool = True) -> None:
        """
        Load configuration from file.

        Args:
            use_defaults: If True, merge with default configuration.
                         Default is True.

        Raises:
            ConfigurationError: If the configuration file does not exist
                               or cannot be parsed.

        Example:
            >>> config = ConfigManager('config.yaml')
            >>> config.load()
            >>> print(config.config)
            {'template_dir': './templates', ...}
        """
        if not self.config_path:
            # Use defaults only
            self.config = self.DEFAULT_CONFIG.copy() if use_defaults else {}
            return

        if not self.config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                file_config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration file: {e}")

        # Merge with defaults
        if use_defaults:
            self.config = self._merge_config(self.DEFAULT_CONFIG.copy(), file_config)
        else:
            self.config = file_config

    def validate(self) -> bool:
        """
        Validate the loaded configuration.

        Returns:
            True if configuration is valid.

        Raises:
            ConfigurationError: If configuration validation fails.

        Example:
            >>> config = ConfigManager('config.yaml')
            >>> config.load()
            >>> config.validate()
            True
        """
        if not self.config:
            raise ConfigurationError("Configuration not loaded")

        # Check required keys
        required_keys = ["template_dir"]
        for key in required_keys:
            if key not in self.config:
                raise ConfigurationError(f"Missing required configuration key: {key}")

        # Validate template_dir exists
        template_dir = Path(self.config["template_dir"])
        if not template_dir.exists():
            raise ConfigurationError(f"Template directory does not exist: {template_dir}")

        return True

    def get(self, key: str, default: Optional[Any] = None, required: bool = False) -> Any:
        """
        Get a configuration value by key.

        Supports nested keys using dot notation (e.g., 'templates.daily-note.enabled').

        Args:
            key: The configuration key to retrieve.
            default: Default value if key is not found.
            required: If True, raises error when key is not found.

        Returns:
            The configuration value.

        Raises:
            ConfigurationError: If key is required but not found.

        Example:
            >>> config = ConfigManager('config.yaml')
            >>> config.load()
            >>> value = config.get('template_dir')
            >>> print(value)
            './templates'

            >>> nested = config.get('templates.daily-note.enabled')
            >>> print(nested)
            True
        """
        if not self.config:
            raise ConfigurationError("Configuration not loaded")

        # Support nested keys with dot notation
        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if required:
                raise ConfigurationError(f"Required configuration key not found: {key}")
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Supports nested keys using dot notation.

        Args:
            key: The configuration key to set.
            value: The value to set.

        Example:
            >>> config = ConfigManager()
            >>> config.load()
            >>> config.set('template_dir', './my-templates')
            >>> config.get('template_dir')
            './my-templates'
        """
        if not self.config:
            self.config = {}

        # Support nested keys with dot notation
        keys = key.split(".")
        current = self.config

        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Set the final value
        current[keys[-1]] = value

    def save(self, path: Optional[str] = None) -> None:
        """
        Save configuration to a YAML file.

        Args:
            path: Path to save configuration. If None, uses the original
                  config_path.

        Raises:
            ConfigurationError: If no path is specified and config_path
                               is not set.

        Example:
            >>> config = ConfigManager()
            >>> config.load()
            >>> config.set('template_dir', './my-templates')
            >>> config.save('new-config.yaml')
        """
        save_path = Path(path) if path else self.config_path

        if not save_path:
            raise ConfigurationError("No path specified for saving configuration")

        try:
            # Ensure parent directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries recursively.

        Args:
            base: Base configuration dictionary.
            override: Override configuration dictionary.

        Returns:
            Merged configuration dictionary.
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def reload(self, use_defaults: bool = True) -> None:
        """
        Reload configuration from file.

        Args:
            use_defaults: If True, merge with default configuration.

        Example:
            >>> config = ConfigManager('config.yaml')
            >>> config.load()
            >>> # ... file changes ...
            >>> config.reload()
        """
        self.config = {}
        self.load(use_defaults=use_defaults)
