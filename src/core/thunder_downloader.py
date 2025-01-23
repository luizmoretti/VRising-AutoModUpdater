"""
Module for downloading mods from Thunderstore.
"""
from pathlib import Path
import time
import re
import logging
import shutil
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import Optional
import datetime

from ..config.config import Config, setup_logging
from ..utils.helpers import setup_chrome_driver, load_json_data, save_json_data

logger = setup_logging(__name__)

class ThunderModsDownloader:
    """
    A class to download mods from Thunderstore.
    
    This class is responsible for:
    - Downloading updated mods from Thunderstore
    - Extracting version information
    - Updating mod metadata
    """
    
    def __init__(self):
        """Initialize ThunderModsDownloader."""
        self.config = Config()
        self.driver = setup_chrome_driver()
        
    def _wait_for_download(self, version_text: str, timeout: int = 30) -> Optional[Path]:
        """
        Wait for a file to be downloaded.
        
        Args:
            version_text: Version text to match in filename
            timeout: Maximum time to wait in seconds
            
        Returns:
            Optional[Path]: Path to downloaded file if found, None otherwise
        """
        elapsed = 0
        while elapsed < timeout:
            for entry in self.config.TEMP_DIR.iterdir():
                if entry.name.startswith(version_text) and entry.name.endswith('.zip'):
                    return entry
            time.sleep(1)
            elapsed += 1
        return None

    def _extract_version(self, mod_name: str) -> str:
        """
        Extract version information from the mod page.
        
        Args:
            mod_name: Name of the mod
            
        Returns:
            str: Version string
        """
        try:
            version_element = self.driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]'
            )
            version_text = version_element.text
            logger.info(f'Raw version text for {mod_name}: {version_text}')
            
            if version_match := re.findall(r'\w+\-\w+\-(\d.+)', version_text):
                version = version_match[0]
                logger.info(f'Parsed version for {mod_name}: {version}')
                return version
                
        except NoSuchElementException:
            logger.warning(f'Could not find version element for {mod_name}')
        except Exception as e:
            logger.error(f'Error extracting version: {str(e)}')
            
        return "0.0.0"

    def download_mods(self) -> None:
        """
        Download mods that need updates.
        """
        try:
            mods_data = load_json_data(self.config.MODS_JSON)
            
            for mod in mods_data:
                if not mod['updated']:
                    continue
                    
                logger.info(f'Updating module {mod["name"]}')
                self.driver.get(mod['ref'])
                time.sleep(1)
                
                # Get version and click download
                version = self._extract_version(mod['name'])
                download_button = self.driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/a'
                )
                download_button.click()
                
                # Wait for download
                version_text = f"{mod['name']}-{version}"
                if downloaded_file := self._wait_for_download(version_text):
                    logger.info(f'Downloaded file: {downloaded_file}')
                    
                    # Update mod metadata
                    mod['version'] = version
                    mod['data'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    mod['updated'] = False
                    logger.info(f'Updated {mod["name"]} to version {version}')
                else:
                    logger.warning(f'Download failed for {mod["name"]}')
            
            # Save updated metadata
            save_json_data(mods_data, self.config.MODS_JSON)
            
            # Create backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            backup_path = self.config.MODS_JSON.parent / f'mods_{timestamp}.json'
            shutil.copy(self.config.MODS_JSON, backup_path)
            logger.info(f'Created backup: {backup_path}')
            
        except Exception as e:
            logger.error(f'Error downloading mods: {str(e)}')
            raise
        finally:
            self.driver.quit()
