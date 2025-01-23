"""
Module for checking and managing local mod directory.
"""
from pathlib import Path
import time
from typing import List, Dict, Any
import logging

from ..config.config import Config, setup_logging
from ..utils.helpers import load_json_data, save_json_data

logger = setup_logging(__name__)

class LocalDirChecker:
    """
    A class to check and manage local mod directory for V-Rising game.
    
    This class is responsible for:
    - Monitoring local mod directory for changes
    - Comparing local mods with remote versions
    - Updating mod status in JSON configuration
    """
    
    def __init__(self) -> None:
        """Initialize LocalDirChecker with configuration."""
        self.config = Config()
        self.config.validate()
        
    def _rename_bloody_core(self, filename: str) -> str:
        """
        Handle special case for Bloody.Core.dll renaming.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Renamed filename if necessary, original filename otherwise
        """
        if filename == 'Bloody.Core.dll':
            logger.info(f"Renaming mod: {filename} -> BloodyCore.dll")
            return 'BloodyCore.dll'
        return filename

    def get_local_files(self) -> List[Dict[str, Any]]:
        """
        Get information about files in the local directory.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing file information
        """
        files_data = []
        
        for entry in self.config.LOCAL_DIR.iterdir():
            if entry.is_file():
                file_data = {
                    "name": self._rename_bloody_core(entry.name),
                    "timestamp": entry.stat().st_mtime,
                }
                files_data.append(file_data)
                logger.debug(f"Found file: {file_data['name']}")
                
        return sorted(files_data, key=lambda x: x['timestamp'], reverse=True)

    def update_mods_status(self) -> None:
        """
        Update the status of mods by comparing local files with JSON data.
        """
        try:
            files_data = self.get_local_files()
            mods_data = load_json_data(self.config.MODS_JSON)
            
            updates_needed = False
            for file_data in files_data:
                for mod in mods_data:
                    if file_data['name'] == mod['name']:
                        mod_timestamp = time.mktime(
                            time.strptime(mod['data'], '%m-%d-%Y')
                        )
                        
                        if file_data['timestamp'] >= mod_timestamp:
                            mod['updated'] = False
                            logger.info(f"Mod {mod['name']} is up to date")
                        else:
                            mod['updated'] = True
                            updates_needed = True
                            logger.info(f"Mod {mod['name']} needs update")
            
            # Save updated JSON if necessary
            if updates_needed:
                save_json_data(mods_data, self.config.MODS_JSON)
                logger.info("Mods status updated in JSON file")
            else:
                logger.info("No updates needed")
                
        except Exception as e:
            logger.error(f"Error updating mods status: {str(e)}")
            raise
