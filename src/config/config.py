"""
Configuration module for the V-Rising Auto Mod Updater.
"""
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

class Config:
    """Base configuration class."""
    
    # FTP Configuration
    FTP_HOST = os.getenv("HOST", "")
    FTP_USERNAME = os.getenv("USERNAME", "")
    FTP_PASSWORD = os.getenv("PASSWORD", "")
    FTP_TARGET_DIR = os.getenv("TARGET_DIR", "")
    
    # Local Configuration
    LOCAL_DIR = Path(os.getenv("LOCAL_DIR", ""))
    MODS_JSON = DATA_DIR / "mods.json"
    
    # Thunderstore Configuration
    THUNDERSTORE_URL = "https://thunderstore.io/c/v-rising/"
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings."""
        if not cls.LOCAL_DIR or not cls.LOCAL_DIR.exists():
            raise ValueError(f"Invalid LOCAL_DIR: {cls.LOCAL_DIR}")
        
        if not all([cls.FTP_HOST, cls.FTP_USERNAME, cls.FTP_PASSWORD, cls.FTP_TARGET_DIR]):
            raise ValueError("Missing FTP configuration")

def setup_logging(name: str) -> logging.Logger:
    """
    Set up logging configuration for a module.
    
    Args:
        name: Name of the logger (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatters and handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOGS_DIR / f"{name}.log",
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
