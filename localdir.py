import os
import time
import json
import datetime
from dotenv import load_dotenv

load_dotenv()


class LocalDirChecker:
    def get_local_local_dir(local_dir=None):
        """
        Função que lista os arquivos em um local_diretório especificado.

        Argumentos:
            local_diretorio: O caminho do local_diretório que você deseja listar os arquivos.

        Retorna:
            Uma lista de nomes de arquivos.

        """
        #variables
        local_dir = str(os.getenv('LOCAL_DIR'))


        # Check if the local_directory exists
        if not os.path.exists(local_dir):
            raise OSError(f"local_diretorio não encontrado {local_dir}")

        # Returns a list of files
        files = os.listdir(local_dir)

        files_data = []

        for file in files:
            file_data = {

                "name": file,
                "timestamp": os.path.getmtime(local_dir + "/" + file),

                }
            if file == 'Bloody.Core.dll':
                #Exclude '.' from Bloody.Core.dll name
                file_data['name'] = file.replace('Bloody.Core.dll', 'BloodyCore.dll')
                #Print mod that has been renamed from Bloody.Core.dll to BloodyCore.dll
                print("Mod Renamed: " + file)
            else:
                print(f"Nothing to changes in " + f"{file}\n")
                
            #add file data to list
            files_data.append(file_data)

        #sorts the list by timestamp
        files_data.sort(key=lambda x: x['timestamp'], reverse=True)

        #prints the sorted files
        for file_data in files_data:
            print(file_data['name'] + " - " + time.ctime(file_data['timestamp']) + " | Uptodate! ")

        #open json file and compare timestamps of files in local_dir with data in json
        with open("json/mods.json", "r") as f:
            datajson = json.load(f)
            for file_data in files_data:
                for mod in datajson:
                    if file_data['name'] == mod['name']:
                        if file_data['timestamp'] >= datetime.datetime.strptime(mod['data'], '%Y-%m-%d').timestamp(): 
                            isupdate = mod['updated'] = False
                        else:
                            isupdate = mod['updated'] = True


        #If var isupdate is true, update key {updated} in json file with True value and write json file with new value of updated key if false do nothing
        if isupdate == True:
            for mod in datajson:
                if mod['name'] == file_data['name']:
                    mod['updated'] = True
            with open("json/mods.json", "w") as f:
                json.dump(datajson, f, indent=4)
            print("Locallocal_dir Done!")
        else:
            print(f"O {file_data['name']} não precisa ser atualizado")
            print("Locallocal_dir Done!")

#Run class
LocalDirChecker.get_local_local_dir()