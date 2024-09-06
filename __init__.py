import subprocess
import sys
import os
import glob

def callHelpers():
    script_paths = [
        os.path.join(os.path.dirname(__file__), 'thunderchecker.py'),
        os.path.join(os.path.dirname(__file__), 'localdir.py'),
        os.path.join(os.path.dirname(__file__), 'thunderdownload.py'),
        os.path.join(os.path.dirname(__file__), 'unzipfiles.py')
    ]
    
    for script_path in script_paths:
        result = subprocess.run([sys.executable, script_path])
        if result.returncode != 0:
            print(f"Script {script_path} failed with return code {result.returncode}")
            break

    # Manter apenas o mods.json e o JSON com o último timestamp
    json_files = glob.glob(os.path.join(os.path.dirname(__file__), 'json', 'mods_*.json'))
    if json_files:
        latest_json = max(json_files, key=os.path.getctime)
        for json_file in json_files:
            if json_file != latest_json:
                os.remove(json_file)
        print(f"Kept the latest JSON file: {os.path.basename(latest_json)}")
    
if __name__ == "__main__":
    callHelpers()
