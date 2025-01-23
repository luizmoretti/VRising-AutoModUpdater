"""
Utility functions for the V-Rising Auto Mod Updater.
"""
from typing import Dict, Any
import datetime
import re
from pathlib import Path
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def format_relative_date(relative_date: str) -> str:
    """
    Convert relative time strings to formatted dates.
    
    Args:
        relative_date: String containing relative time information
        
    Returns:
        str: Formatted date string in MM-DD-YYYY format
    """
    now = datetime.datetime.now()
    
    time_mapping = {
        "a day ago": now - datetime.timedelta(days=1),
        "1 minute ago": now - datetime.timedelta(minutes=1),
        "a minute ago": now - datetime.timedelta(minutes=1),
        "an hour ago": now - datetime.timedelta(hours=1),
        "a week ago": now - datetime.timedelta(weeks=1),
        "a month ago": now - datetime.timedelta(weeks=4),
        "a year ago": now - datetime.timedelta(weeks=52)
    }
    
    # Check direct mappings
    for key, value in time_mapping.items():
        if relative_date == f"Last updated: {key}":
            return value.strftime("%m-%d-%Y")
    
    # Parse relative time patterns
    patterns = [
        (r"(\d+) minutes ago", lambda x: now - datetime.timedelta(minutes=int(x))),
        (r"(\d+) hours ago", lambda x: now - datetime.timedelta(hours=int(x))),
        (r"(\d+) days ago", lambda x: now - datetime.timedelta(days=int(x))),
        (r"(\d+) weeks ago", lambda x: now - datetime.timedelta(weeks=int(x))),
        (r"(\d+) months ago", lambda x: now - datetime.timedelta(weeks=int(x) * 4))
    ]
    
    for pattern, time_func in patterns:
        if match := re.search(f"Last updated: {pattern}", relative_date):
            return time_func(match.group(1)).strftime("%m-%d-%Y")
            
    return relative_date

def setup_chrome_driver() -> webdriver.Chrome:
    """
    Configure and return a Chrome WebDriver instance.
    
    Returns:
        webdriver.Chrome: Configured WebDriver instance
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def load_json_data(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dict[str, Any]: Loaded JSON data
    """
    if not file_path.exists():
        return {}
    
    with file_path.open('r') as f:
        return json.load(f)

def save_json_data(data: Dict[str, Any], file_path: Path) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the JSON file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('w') as f:
        json.dump(data, f, indent=4)
