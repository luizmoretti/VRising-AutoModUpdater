import os
import sys
import json
import time
import datetime
import re
import logging
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class ThunderModsDownload:
    def __init__(self, driver, download_dir):
        self.driver = driver
        self.download_dir = download_dir

    @staticmethod
    def driveroptions():
        options = Options()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        #options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        
        #Set default download path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        download_path = os.path.join(script_dir, 'temp')
        options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "profile.default_content_settings.popups": 0
        })
        return options

    def thunderdownload(self):
        with open("json/mods.json", "r") as f:
            datajson = json.load(f)

        self.driver = webdriver.Chrome(options=ThunderModsDownload.driveroptions())

        for data in datajson:
            nome_arquivo = data['name']
            link_referencia = data['ref']
            if data['updated']:
                logging.info(f'Updating module {nome_arquivo}')
                self.driver.get(link_referencia)
                time.sleep(1)

                version_element = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]')
                version_text = version_element.text
                logging.info(f'Raw version text for {nome_arquivo}: {version_text}')
                version_match = re.findall(r'\w+\-\w+\-(\d.+)', version_text)
                if version_match:
                    version = version_match[0]
                    logging.info(f'Parsed version for {nome_arquivo}: {version}')
                else:
                    version = "0.0.0"
                    logging.warning(f'Could not parse version for {nome_arquivo}, setting as {version}')

                download_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/a')
                download_button.click()

                # Wait until the download is complete
                timeout = 10  # Maximum waiting time in seconds
                elapsed = 0

                while not any(entry.name.startswith(version_text) and entry.name.endswith('.zip') for entry in os.scandir(self.download_dir)):
                    time.sleep(2)
                    elapsed += 2
                    if elapsed > timeout:
                        logging.warning(f"Timeout waiting for {version_text} to download.")
                        break

                downloaded_file = next((entry.name for entry in os.scandir(self.download_dir) if entry.name.startswith(version_text) and entry.name.endswith('.zip')), None)

                if downloaded_file:
                    logging.info(f'Downloaded file found for {version_text}: {downloaded_file}')
                    
                    #Update the version and date of the mod
                    for mod in datajson:
                        if mod['name'] == nome_arquivo:
                            mod['version'] = version
                            mod['data'] = datetime.datetime.now().strftime("%Y-%m-%d")
                            mod['updated'] = False  #Mark as updated
                            logging.info(f'Updated {nome_arquivo} to version {version}\n')
                            break
                else:
                    logging.warning(f'Downloaded file not found for {version_text} after waiting.')

        #Update the JSON file after all downloads are complete
        with open("json/mods.json", "w") as f:
            json.dump(datajson, f, indent=4)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_json_path = f'json/mods_{timestamp}.json'
        shutil.copy("json/mods.json", new_json_path)
        logging.info(f'Created {new_json_path}')

# Initiate ThunderModsDownload
download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
start = ThunderModsDownload(driver=None, download_dir=download_dir)
start.thunderdownload()
