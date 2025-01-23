import os
import zipfile
import shutil
import json
import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

load_dotenv()

class UnzipFiles:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_folder = os.path.join(script_dir, 'temp')
        self.local_dir = str(os.getenv('LOCAL_DIR'))
        if not self.local_dir:
            logging.error("LOCAL_DIR is not set in the environment variables.")
            raise ValueError("LOCAL_DIR is not set in the environment variables.")

    def unzip_file(self, filename):
        zip_path = os.path.join(self.temp_folder, filename)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_folder)
        logging.info(f"Extracted {filename}")

    def unzip_files(self):
        if not os.path.exists(self.temp_folder):
            logging.error(f"The folder {self.temp_folder} does not exist.")
            return

        zip_files = [f for f in os.listdir(self.temp_folder) if f.endswith('.zip')]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.unzip_file, filename) for filename in zip_files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error extracting file: {e}")

        logging.info("Unzipping complete.")

    def move_file(self, mod_name):
        source_path = os.path.join(self.temp_folder, mod_name)
        if os.path.exists(source_path) and mod_name.endswith('.dll'):
            dest_path = os.path.join(self.local_dir, mod_name)
            shutil.move(source_path, dest_path)
            logging.info(f"Moved {mod_name} to {self.local_dir}")
        else:
            logging.warning(f"{mod_name} not found in extracted files or is not a .dll file.")

    def move_files(self):
        with open("json/mods.json", "r") as f:
            mods_info = json.load(f)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.move_file, mod['name']) for mod in mods_info if mod['name'].endswith('.dll')]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error moving file: {e}")

    def clean_temp_folder(self):
        for filename in os.listdir(self.temp_folder):
            file_path = os.path.join(self.temp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                logging.info(f"Deleted {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    unzipper = UnzipFiles()
    unzipper.unzip_files()
    unzipper.move_files()
    unzipper.clean_temp_folder()
