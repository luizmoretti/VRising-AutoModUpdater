"""
Module for checking mod updates on Thunderstore.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Dict, Any
import logging

from ..config.config import Config, setup_logging
from ..utils.helpers import setup_chrome_driver, format_relative_date, save_json_data

logger = setup_logging(__name__)

class ThunderModsChecker:
    """
    A class to check for mod updates on the Thunderstore platform.
    
    This class is responsible for:
    - Scraping mod information from Thunderstore
    - Parsing mod metadata
    - Saving mod information to JSON
    """
    
    def __init__(self):
        """Initialize ThunderModsChecker."""
        self.config = Config()
        self.driver = setup_chrome_driver()
        self.mods_info: List[Dict[str, Any]] = []
        
    def check_updates(self) -> None:
        """
        Check for mod updates on Thunderstore.
        """
        try:
            self.driver.get(self.config.THUNDERSTORE_URL)
            
            package_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".package-list"))
            )
            
            cards = package_list.find_elements(By.CSS_SELECTOR, ".mb-2")
            logger.info(f"Found {len(cards)} mod cards")
            
            for card in cards:
                try:
                    name = card.find_element(By.TAG_NAME, "h5").text.strip()
                    update_data = card.find_element(By.TAG_NAME, "small").text.strip()
                    href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    # Format mod name
                    formatted_name = f"{name.replace(' ', '')}.dll"
                    formatted_date = format_relative_date(update_data)
                    
                    mod_info = {
                        "name": formatted_name,
                        "data": formatted_date,
                        "ref": href,
                        "updated": False,
                        "version": "0.0.0"
                    }
                    
                    self.mods_info.append(mod_info)
                    logger.debug(f"Processed mod: {formatted_name}")
                    
                except NoSuchElementException as e:
                    logger.error(f"Error processing mod card: {str(e)}")
                    continue
            
            # Save mods information
            save_json_data(self.mods_info, self.config.MODS_JSON)
            logger.info(f"Saved {len(self.mods_info)} mods to {self.config.MODS_JSON}")
            
        except TimeoutException:
            logger.error("Timeout waiting for package list to load")
            raise
        except Exception as e:
            logger.error(f"Error checking updates: {str(e)}")
            raise
        finally:
            self.driver.quit()
