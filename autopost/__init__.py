"""
Automated Daily Poster Bot

A Python application for automated content posting with intelligent scheduling,
multiple content sources, and comprehensive logging.

Author: Your Name
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Core imports for easy access
from .core.bot import AutomatedPosterBot
from .config.settings import Config
from .__main__ import main

__all__ = ["AutomatedPosterBot", "Config", "main", "__version__", "__author__", "__email__"]
