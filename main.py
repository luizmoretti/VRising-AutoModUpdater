"""
Main entry point for V-Rising Auto Mod Updater.
"""
import logging
from src.config.config import setup_logging
from src.core import (
    LocalDirChecker,
    ThunderModsChecker,
    ThunderModsDownloader,
    FileManager
)

logger = setup_logging(__name__)

def main():
    """
    Main function to run the mod update process.
    """
    try:
        # Check local directory
        logger.info("Checking local directory...")
        local_checker = LocalDirChecker()
        local_checker.update_mods_status()
        
        # Check for updates
        logger.info("Checking for updates on Thunderstore...")
        thunder_checker = ThunderModsChecker()
        thunder_checker.check_updates()
        
        # Download updates
        logger.info("Downloading updates...")
        downloader = ThunderModsDownloader()
        downloader.download_mods()
        
        # Process files
        logger.info("Processing downloaded files...")
        file_manager = FileManager()
        file_manager.process_files()
        
        logger.info("Update process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during update process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
