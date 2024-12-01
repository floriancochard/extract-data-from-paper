"""
Module for logging configuration and setup.
Provides utilities to create and configure loggers with consistent formatting.
"""

import os
import logging
import logging.config
from typing import Dict, Optional


class Log:
    """Class containing logging configuration utilities."""

    def __init__(self, log_path: Optional[str] = None):
        """
        Initialize Log class.

        Args:
            log_path: Optional path for log file output
        """
        self.log_path = log_path
        self.default_config = self._get_default_config()

    def create_logger(self, name: str) -> logging.Logger:
        """
        Create and configure a logger instance.

        Args:
            name: Name of the logger to create

        Returns:
            Configured logger instance

        Raises:
            ValueError: If logger name is empty or invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Logger name must be a non-empty string")

        logging.config.dictConfig(self.default_config)
        return logging.getLogger(name)

    def _get_default_config(self) -> Dict:
        """
        Get default logging configuration.

        Returns:
            Dictionary containing logging configuration
        """
        config = {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(message)s"
                },
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "default": {
                    "level": "DEBUG",
                    "handlers": ["console"]
                }
            },
            "disable_existing_loggers": False
        }

        # Add file handler if log path is provided
        if self.log_path:
            config["handlers"]["file"] = {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": self.log_path,
                "maxBytes": 1024,
                "backupCount": 0
            }
            config["loggers"]["default"]["handlers"].append("file")

        return config
