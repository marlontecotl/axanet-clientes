"""
Configuration Management for Axanet Client Manager
=================================================

This module handles all configuration settings for the application, including
file paths, logging configuration, and environment-specific settings.

Features:
---------
- Environment variable support for flexible deployment
- Default values with override capability
- Centralized configuration management
- Validation of configuration values
- Different configurations for development, testing, and production

Educational Notes for Students:
-------------------------------
1. Centralized configuration makes applications easier to maintain
2. Environment variables allow for secure and flexible deployment
3. Configuration validation prevents runtime errors
4. Type hints improve configuration reliability
5. Default values ensure the application works out of the box

Design Patterns Used:
---------------------
- Singleton Pattern: Single configuration instance throughout the application
- Factory Pattern: Different configurations for different environments
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging


@dataclass
class DatabaseConfig:
    """Configuration for file-based data storage."""
    base_directory: str = "axanet_clients_data"
    file_extension: str = ".txt"
    encoding: str = "utf-8"
    
    @property
    def full_path(self) -> Path:
        """Get the full path to the data directory."""
        return Path(self.base_directory).resolve()


@dataclass
class LoggingConfig:
    """Configuration for application logging."""
    level: str = "INFO"
    file_name: str = "axanet_client_manager.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    max_file_size_mb: int = 10
    backup_count: int = 5
    
    @property
    def log_level(self) -> int:
        """Convert string log level to logging constant."""
        return getattr(logging, self.level.upper(), logging.INFO)


@dataclass
class AppConfig:
    """Main application configuration."""
    app_name: str = "Axanet Client Manager"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Component configurations
    database: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()


class ConfigManager:
    """
    Manages application configuration with environment variable support.
    
    This class provides a centralized way to manage all application settings,
    with support for environment variables and different deployment environments.
    
    Educational Notes:
        - Singleton pattern ensures consistent configuration across the app
        - Environment variables allow secure deployment without code changes
        - Configuration validation prevents common deployment issues
        - Type conversion ensures proper data types for settings
    """
    
    _instance: Optional['ConfigManager'] = None
    _config: Optional[AppConfig] = None
    
    def __new__(cls) -> 'ConfigManager':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager."""
        if self._config is None:
            self._config = self._load_config()
    
    def _load_config(self) -> AppConfig:
        """
        Load configuration from environment variables and defaults.
        
        Returns:
            AppConfig: Loaded configuration
            
        Educational Note:
            This method demonstrates how to read environment variables
            with fallback to default values, providing flexibility
            for different deployment scenarios.
        """
        # Load environment-specific settings
        environment = os.getenv("AXANET_ENV", "development")
        debug = self._get_bool_env("AXANET_DEBUG", False)
        
        # Database configuration
        db_config = DatabaseConfig(
            base_directory=os.getenv("AXANET_DATA_DIR", "axanet_clients_data"),
            file_extension=os.getenv("AXANET_FILE_EXT", ".txt"),
            encoding=os.getenv("AXANET_ENCODING", "utf-8")
        )
        
        # Logging configuration  
        log_config = LoggingConfig(
            level=os.getenv("AXANET_LOG_LEVEL", "INFO"),
            file_name=os.getenv("AXANET_LOG_FILE", "axanet_client_manager.log"),
            max_file_size_mb=self._get_int_env("AXANET_LOG_MAX_SIZE_MB", 10),
            backup_count=self._get_int_env("AXANET_LOG_BACKUP_COUNT", 5)
        )
        
        # Main application configuration
        config = AppConfig(
            app_name=os.getenv("AXANET_APP_NAME", "Axanet Client Manager"),
            version=os.getenv("AXANET_VERSION", "1.0.0"),
            debug=debug,
            environment=environment,
            database=db_config,
            logging=log_config
        )
        
        # Validate configuration
        self._validate_config(config)
        
        return config
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer value from environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    def _validate_config(self, config: AppConfig) -> None:
        """
        Validate configuration values.
        
        Args:
            config (AppConfig): Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
            
        Educational Note:
            Configuration validation catches issues early in the application
            lifecycle, preventing runtime errors and providing clear feedback.
        """
        # Validate environment
        valid_environments = ["development", "testing", "production"]
        if config.environment not in valid_environments:
            raise ValueError(f"Invalid environment: {config.environment}. "
                           f"Must be one of: {valid_environments}")
        
        # Validate logging level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config.logging.level.upper() not in valid_log_levels:
            raise ValueError(f"Invalid log level: {config.logging.level}. "
                           f"Must be one of: {valid_log_levels}")
        
        # Validate file extension
        if not config.database.file_extension.startswith('.'):
            raise ValueError("File extension must start with a dot")
        
        # Validate numeric values
        if config.logging.max_file_size_mb <= 0:
            raise ValueError("Log file max size must be positive")
        
        if config.logging.backup_count < 0:
            raise ValueError("Log backup count cannot be negative")
    
    @property
    def config(self) -> AppConfig:
        """Get the current configuration."""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def get_data_directory(self) -> Path:
        """Get the full path to the data directory."""
        return self.config.database.full_path
    
    def ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        data_dir = self.get_data_directory()
        data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_client_file_path(self, normalized_name: str) -> Path:
        """
        Get the file path for a client.
        
        Args:
            normalized_name (str): Normalized client name
            
        Returns:
            Path: Full path to client file
        """
        filename = f"{normalized_name}{self.config.database.file_extension}"
        return self.get_data_directory() / filename
    
    def reload_config(self) -> None:
        """Reload configuration from environment variables."""
        self._config = self._load_config()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
            
        Educational Note:
            This method is useful for debugging, logging, and creating
            configuration reports or documentation.
        """
        return {
            "app_name": self.config.app_name,
            "version": self.config.version,
            "debug": self.config.debug,
            "environment": self.config.environment,
            "database": {
                "base_directory": self.config.database.base_directory,
                "file_extension": self.config.database.file_extension,
                "encoding": self.config.database.encoding,
                "full_path": str(self.config.database.full_path)
            },
            "logging": {
                "level": self.config.logging.level,
                "file_name": self.config.logging.file_name,
                "max_file_size_mb": self.config.logging.max_file_size_mb,
                "backup_count": self.config.logging.backup_count
            }
        }


# Global configuration instance
config_manager = ConfigManager()

# Convenience functions for easy access
def get_config() -> AppConfig:
    """Get the application configuration."""
    return config_manager.config

def get_data_directory() -> Path:
    """Get the data directory path."""
    return config_manager.get_data_directory()

def get_client_file_path(normalized_name: str) -> Path:
    """Get the file path for a client."""
    return config_manager.get_client_file_path(normalized_name)