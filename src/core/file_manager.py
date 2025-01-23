"""
Module for managing file operations (unzip, move, cleanup).
"""
import zipfile
import shutil
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from config.config import Config, setup_logging
from utils.helpers import load_json_data

logger = setup_logging(__name__)

class FileManager:
    """
    A class to manage file operations for mods.
    
    This class is responsible for:
    - Extracting downloaded mod archives
    - Moving mod files to the game directory
    - Cleaning up temporary files
    """
    
    def __init__(self):
        """Initialize FileManager."""
        self.config = Config()
        
    def _unzip_file(self, zip_path: Path) -> None:
        """
        Extract a zip file to the temporary directory.
        
        Args:
            zip_path: Path to the zip file
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.config.TEMP_DIR)
            logger.info(f"Extracted {zip_path.name}")
        except Exception as e:
            logger.error(f"Error extracting {zip_path.name}: {str(e)}")
            raise

    def unzip_files(self) -> None:
        """
        Extract all zip files in the temporary directory.
        """
        zip_files = list(self.config.TEMP_DIR.glob('*.zip'))
        if not zip_files:
            logger.info("No zip files found to extract")
            return
            
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._unzip_file, zip_path)
                for zip_path in zip_files
            ]
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Failed to process zip file: {str(e)}")

    def _move_file(self, mod_name: str) -> None:
        """
        Move a mod file to the game directory.
        
        Args:
            mod_name: Name of the mod file
        """
        source_path = self.config.TEMP_DIR / mod_name
        if source_path.exists() and mod_name.endswith('.dll'):
            dest_path = self.config.LOCAL_DIR / mod_name
            shutil.move(source_path, dest_path)
            logger.info(f"Moved {mod_name} to {self.config.LOCAL_DIR}")
        else:
            logger.warning(f"{mod_name} not found or is not a .dll file")

    def move_files(self) -> None:
        """
        Move all mod files to the game directory.
        """
        mods_data = load_json_data(self.config.MODS_JSON)
        dll_files = [
            mod['name'] for mod in mods_data
            if mod['name'].endswith('.dll')
        ]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._move_file, dll_file)
                for dll_file in dll_files
            ]
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Failed to move file: {str(e)}")

    def clean_temp_folder(self) -> None:
        """
        Remove all files from the temporary directory.
        """
        for item in self.config.TEMP_DIR.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
                logger.info(f"Deleted {item}")
            except Exception as e:
                logger.error(f"Failed to delete {item}: {str(e)}")

    def process_files(self) -> None:
        """
        Process all files: unzip, move, and cleanup.
        """
        try:
            self.unzip_files()
            self.move_files()
            self.clean_temp_folder()
        except Exception as e:
            logger.error(f"Error processing files: {str(e)}")
            raise
