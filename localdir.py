import os
import time
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

class LocalDirChecker:
    @staticmethod
    def get_local_dir():
        """
        Function that lists files in a specified local directory.

        Arguments:
            local_dir: The path of the directory you want to list the files from.

        Returns:
            A list of file names.
        """
        # Variables
        local_dir = str(os.getenv('LOCAL_DIR'))

        # Check if the directory exists
        if not os.path.exists(local_dir):
            raise OSError(f"Directory not found: {local_dir}")

        # Use os.scandir for better performance
        with os.scandir(local_dir) as entries:
            files_data = []
            for entry in entries:
                if entry.is_file():
                    file_data = {
                        "name": entry.name,
                        "timestamp": entry.stat().st_mtime,
                    }
                    if entry.name == 'Bloody.Core.dll':
                        # Remove '.' from Bloody.Core.dll name
                        file_data['name'] = entry.name.replace('Bloody.Core.dll', 'BloodyCore.dll')
                        # Print mod that has been renamed from Bloody.Core.dll to BloodyCore.dll
                        print("Mod Renamed: " + entry.name)
                    else:
                        print(f"Nothing to change in {entry.name}\n")
                        
                    # Add file data to list
                    files_data.append(file_data)

        # Sort the list by timestamp
        files_data.sort(key=lambda x: x['timestamp'], reverse=True)

        # Print the sorted files
        for file_data in files_data:
            print(file_data['name'] + " - " + time.ctime(file_data['timestamp']) + " | Uptodate! ")

        # Open JSON file and compare timestamps of files in local_dir with data in JSON
        with open("json/mods.json", "r") as f:
            datajson = json.load(f)
        
        isupdate = False
        for file_data in files_data:
            for mod in datajson:
                if file_data['name'] == mod['name']:
                    if file_data['timestamp'] >= datetime.datetime.strptime(mod['data'], '%m-%d-%Y').timestamp():
                        mod['updated'] = False
                    else:
                        mod['updated'] = True
                        isupdate = True

        # If isupdate is True, update the {updated} key in the JSON file with the value True and write the JSON file with the new value of the updated key. Otherwise, do nothing
        if isupdate:
            with open("json/mods.json", "w") as f:
                json.dump(datajson, f, indent=4)
            print("LocalDir Done!")
        else:
            print("No updates needed")
            print("LocalDir Done!")

if __name__ == "__main__":
    LocalDirChecker.get_local_dir()
