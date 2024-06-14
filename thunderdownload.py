import os
import sys
import json
import time
import datetime
import re
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class ThunderModsDownload:
    def __init__(self, driver, local_dir_return):
        self.driver = driver
        self.local_dir_return = local_dir_return
        self.session = self.get_session()

    @staticmethod
    def driveroptions():
        options = Options()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        # Set default download path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        download_path = os.path.join(script_dir, 'temp')
        options.add_experimental_option("prefs", { "download.default_directory": download_path })
        return options

    @staticmethod
    def get_session():
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def thunderdownload(self):
        with open("json/mods.json", "r") as f:
            datajson = json.load(f)

        self.driver = webdriver.Chrome(options=ThunderModsDownload.driveroptions())

        def update_mod(data):
            nome_arquivo = data['name']
            link_referencia = data['ref']
            if data['updated']:
                logging.info(f'Updating module {nome_arquivo}')
                self.driver.get(link_referencia)
                time.sleep(1)

                version_element = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]')
                version = version_element.text
                version = re.findall(r'\w+\-\w+\-(\d.+)', version)
                version = version[0]
                logging.info(f'Version: {version}')
                time.sleep(1)

                download = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/a')))
                download.click()
                time.sleep(1)

                data['updated'] = False
                data['version'] = version
                data['data'] = datetime.datetime.now().strftime("%Y-%m-%d")

                with open("json/mods.json", "w") as f:
                    json.dump(datajson, f, indent=4)

                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
                new_json_path = f'json/mods_{timestamp}.json'
                shutil.copy("json/mods.json", new_json_path)
                logging.info(f'Created {new_json_path}')
                logging.info(f'File {nome_arquivo} updated at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            else:
                logging.info(f'Module {nome_arquivo} was already updated at {data["data"]}')

        updates_needed = [data for data in datajson if data['updated']]

        if updates_needed:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(update_mod, data) for data in updates_needed]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f'Error updating mod: {e}')
        else:
            logging.info('Mods are already uptodate')

# Initiate ThunderModsDownload
start = ThunderModsDownload(driver=None, local_dir_return=None)
start.thunderdownload()
