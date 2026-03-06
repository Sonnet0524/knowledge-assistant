#!/usr/bin/env python3
"""
Tests for ConfigManager module.

This module contains comprehensive tests for the ConfigManager class.
"""

import pytest
from pathlib import Path
import yaml
from scripts.config import ConfigManager, ConfigurationError


class TestConfigManagerInit:
    """Tests for ConfigManager initialization."""
    
    def test_init_with_path(self, tmp_path):
        """Test initialization with a configuration file path."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("template_dir: ./templates")
        
        manager = ConfigManager(str(config_path))
        assert manager.config_path == config_path
        assert manager.config == {}
    
    def test_init_without_path(self):
        """Test initialization without a configuration file path."""
        manager = ConfigManager()
        assert manager.config_path is None
        assert manager.config == {}


class TestLoad:
    """Tests for load method."""
    
    def test_load_with_valid_file(self, tmp_path):
        """Test loading a valid configuration file."""
        config_path = tmp_path / "config.yaml"
        config_data = {
            'template_dir': './templates',
            'output_dir': './output',
        }
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load()
        
        assert manager.config['template_dir'] == './templates'
        assert manager.config['output_dir'] == './output'
        # Should include defaults
        assert 'default_author' in manager.config
    
    def test_load_without_defaults(self, tmp_path):
        """Test loading configuration without merging defaults."""
        config_path = tmp_path / "config.yaml"
        config_data = {'template_dir': './my-templates'}
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        
        assert manager.config == config_data
        # Should not include defaults
        assert 'default_author' not in manager.config
    
    def test_load_with_defaults_only(self):
        """Test loading with defaults only (no file)."""
        manager = ConfigManager()
        manager.load()
        
        assert manager.config == ConfigManager.DEFAULT_CONFIG
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises error."""
        manager = ConfigManager('/nonexistent/config.yaml')
        
        with pytest.raises(ConfigurationError, match="Configuration file not found"):
            manager.load()
    
    def test_load_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML raises error."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("invalid: yaml: content: [")
        
        manager = ConfigManager(str(config_path))
        
        with pytest.raises(ConfigurationError, match="Failed to parse"):
            manager.load()
    
    def test_load_empty_file(self, tmp_path):
        """Test loading an empty file."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("")
        
        manager = ConfigManager(str(config_path))
        manager.load()
        
        # Should use defaults
        assert manager.config == ConfigManager.DEFAULT_CONFIG
    
    def test_load_merge_nested_configs(self, tmp_path):
        """Test that nested configurations are merged properly."""
        config_path = tmp_path / "config.yaml"
        config_data = {
            'templates': {
                'daily-note': {
                    'enabled': False,
                }
            }
        }
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load()
        
        # Should merge with defaults
        assert manager.config['templates']['daily-note']['enabled'] is False
        # Other template settings should still be present
        assert 'research-note' in manager.config['templates']


class TestValidate:
    """Tests for validate method."""
    
    @pytest.fixture
    def valid_config(self, tmp_path):
        """Create a valid configuration file."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        
        config_path = tmp_path / "config.yaml"
        config_data = {'template_dir': str(template_dir)}
        config_path.write_text(yaml.dump(config_data))
        
        return config_path
    
    def test_validate_valid_config(self, valid_config, tmp_path):
        """Test validating a valid configuration."""
        manager = ConfigManager(str(valid_config))
        manager.load()
        
        assert manager.validate() is True
    
    def test_validate_without_load(self):
        """Test validating before loading raises error."""
        manager = ConfigManager()
        
        with pytest.raises(ConfigurationError, match="Configuration not loaded"):
            manager.validate()
    
    def test_validate_missing_required_key(self, tmp_path):
        """Test validation with missing required key."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({'output_dir': './output'}))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        
        with pytest.raises(ConfigurationError, match="Missing required configuration key"):
            manager.validate()
    
    def test_validate_nonexistent_template_dir(self, tmp_path):
        """Test validation with non-existent template directory."""
        config_path = tmp_path / "config.yaml"
        config_data = {'template_dir': '/nonexistent/templates'}
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        
        with pytest.raises(ConfigurationError, match="Template directory does not exist"):
            manager.validate()


class TestGet:
    """Tests for get method."""
    
    @pytest.fixture
    def loaded_manager(self, tmp_path):
        """Create a loaded configuration manager."""
        config_path = tmp_path / "config.yaml"
        config_data = {
            'template_dir': './templates',
            'nested': {
                'key': {
                    'value': 42
                }
            }
        }
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        return manager
    
    def test_get_simple_key(self, loaded_manager):
        """Test getting a simple configuration value."""
        value = loaded_manager.get('template_dir')
        assert value == './templates'
    
    def test_get_nested_key(self, loaded_manager):
        """Test getting a nested configuration value with dot notation."""
        value = loaded_manager.get('nested.key.value')
        assert value == 42
    
    def test_get_nonexistent_key_with_default(self, loaded_manager):
        """Test getting a non-existent key with default value."""
        value = loaded_manager.get('nonexistent', default='default_value')
        assert value == 'default_value'
    
    def test_get_nonexistent_key_without_default(self, loaded_manager):
        """Test getting a non-existent key without default."""
        value = loaded_manager.get('nonexistent')
        assert value is None
    
    def test_get_required_key_missing(self, loaded_manager):
        """Test getting a required key that doesn't exist raises error."""
        with pytest.raises(ConfigurationError, match="Required configuration key not found"):
            loaded_manager.get('nonexistent', required=True)
    
    def test_get_without_load(self):
        """Test getting value before loading raises error."""
        manager = ConfigManager()
        
        with pytest.raises(ConfigurationError, match="Configuration not loaded"):
            manager.get('key')
    
    def test_get_nested_key_partial(self, loaded_manager):
        """Test getting a partial nested key returns dict."""
        value = loaded_manager.get('nested.key')
        assert value == {'value': 42}


class TestSet:
    """Tests for set method."""
    
    def test_set_simple_key(self):
        """Test setting a simple configuration value."""
        manager = ConfigManager()
        manager.load()
        
        manager.set('template_dir', './my-templates')
        assert manager.get('template_dir') == './my-templates'
    
    def test_set_nested_key(self):
        """Test setting a nested configuration value."""
        manager = ConfigManager()
        manager.load()
        
        manager.set('nested.key.value', 123)
        assert manager.get('nested.key.value') == 123
    
    def test_set_creates_nested_structure(self):
        """Test that set creates nested structure if needed."""
        manager = ConfigManager()
        manager.config = {}
        
        manager.set('a.b.c.d', 'value')
        assert manager.get('a.b.c.d') == 'value'
        assert manager.config['a']['b']['c']['d'] == 'value'
    
    def test_set_overwrites_existing(self):
        """Test that set overwrites existing values."""
        manager = ConfigManager()
        manager.load()
        
        manager.set('template_dir', './new-templates')
        assert manager.get('template_dir') == './new-templates'


class TestSave:
    """Tests for save method."""
    
    def test_save_to_original_path(self, tmp_path):
        """Test saving configuration to original path."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({'template_dir': './templates'}))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        manager.set('new_key', 'new_value')
        manager.save()
        
        # Read back and verify
        with open(config_path) as f:
            saved_config = yaml.safe_load(f)
        
        assert saved_config['new_key'] == 'new_value'
    
    def test_save_to_new_path(self, tmp_path):
        """Test saving configuration to a new path."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({'template_dir': './templates'}))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        
        new_path = tmp_path / "new-config.yaml"
        manager.save(str(new_path))
        
        assert new_path.exists()
        with open(new_path) as f:
            saved_config = yaml.safe_load(f)
        assert saved_config['template_dir'] == './templates'
    
    def test_save_without_path(self):
        """Test saving without a path raises error."""
        manager = ConfigManager()
        manager.load()
        
        with pytest.raises(ConfigurationError, match="No path specified"):
            manager.save()
    
    def test_save_creates_parent_directories(self, tmp_path):
        """Test that save creates parent directories if needed."""
        config_path = tmp_path / "subdir" / "config.yaml"
        
        manager = ConfigManager()
        manager.load()
        
        manager.save(str(config_path))
        
        assert config_path.exists()


class TestReload:
    """Tests for reload method."""
    
    def test_reload_configuration(self, tmp_path):
        """Test reloading configuration from file."""
        config_path = tmp_path / "config.yaml"
        config_data = {'template_dir': './templates'}
        config_path.write_text(yaml.dump(config_data))
        
        manager = ConfigManager(str(config_path))
        manager.load(use_defaults=False)
        
        # Modify file
        new_data = {'template_dir': './new-templates'}
        config_path.write_text(yaml.dump(new_data))
        
        # Reload
        manager.reload(use_defaults=False)
        
        assert manager.get('template_dir') == './new-templates'


class TestMergeConfig:
    """Tests for _merge_config method."""
    
    def test_merge_simple_values(self):
        """Test merging simple values."""
        manager = ConfigManager()
        manager.load()
        
        base = {'a': 1, 'b': 2}
        override = {'b': 3, 'c': 4}
        result = manager._merge_config(base, override)
        
        assert result == {'a': 1, 'b': 3, 'c': 4}
    
    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        manager = ConfigManager()
        manager.load()
        
        base = {
            'templates': {
                'daily-note': {'enabled': True, 'auto_date': True},
                'research-note': {'enabled': True}
            }
        }
        override = {
            'templates': {
                'daily-note': {'enabled': False}
            }
        }
        result = manager._merge_config(base, override)
        
        assert result['templates']['daily-note']['enabled'] is False
        assert result['templates']['daily-note']['auto_date'] is True
        assert result['templates']['research-note']['enabled'] is True
    
    def test_merge_override_non_dict(self):
        """Test merging when override replaces dict with scalar."""
        manager = ConfigManager()
        manager.load()
        
        base = {'templates': {'daily-note': {'enabled': True}}}
        override = {'templates': 'simple-value'}
        result = manager._merge_config(base, override)
        
        assert result['templates'] == 'simple-value'


class TestIntegration:
    """Integration tests with actual config file."""
    
    def test_load_example_config(self):
        """Test loading the example configuration file."""
        example_path = Path("./config.example.yaml")
        if not example_path.exists():
            pytest.skip("Example config file not found")
        
        manager = ConfigManager(str(example_path))
        manager.load()
        
        # Check expected keys
        assert 'template_dir' in manager.config
        assert 'output_dir' in manager.config
        assert 'templates' in manager.config
        assert 'daily-note' in manager.config['templates']
    
    def test_roundtrip_save_and_load(self, tmp_path):
        """Test saving and loading configuration preserves values."""
        config_path = tmp_path / "config.yaml"
        
        # Create and save
        manager = ConfigManager()
        manager.load()
        manager.set('template_dir', './test-templates')
        manager.set('custom.setting', 'value')
        manager.save(str(config_path))
        
        # Load in new instance
        manager2 = ConfigManager(str(config_path))
        manager2.load(use_defaults=False)
        
        assert manager2.get('template_dir') == './test-templates'
        assert manager2.get('custom.setting') == 'value'
