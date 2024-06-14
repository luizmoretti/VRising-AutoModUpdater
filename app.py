import os
import ftplib
import json
import time
from time import sleep
from dotenv import load_dotenv
import datetime
from init_ import callHelpers

class AutoUpdater:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def load_dotenvv(self):
        #get env variables
        load_dotenv()
        self.host = str(os.getenv('HOST'))
        self.username = str(os.getenv('USERNAME'))
        self.password = str(os.getenv('PASSWORD'))
    
    def connect_ftp(self):
        self.load_dotenvv()
        try:
            ftp = ftplib.FTP(self.host)
            ftp.login(self.username, self.password)
            print(f"Conectado ao servidor FTP {self.host}")
            return ftp
        except ftplib.error as e:
            print(f"Falha ao conectar ao servidor FTP: {e}")
            return None

    def list_files_ftp(self, ftp):
        #Print current directory content
        main_content = ftp.nlst()
        for file in main_content:
            print(file)
    
    def transfer_files(self, ftp, local_dir, current__ftp_dir):
        print("\n-------Transferindo arquivos-------\n")
        
        files_transferidas = []
        
        #Get list of files in local_dir
        files_local = os.listdir(local_dir)
        
        #Get list of files in current__ftp_dir
        files_ftp = ftp.nlst()
        
        #Compare files
        if current__ftp_dir == str(os.getenv('TARGET_DIR')):
            for file in files_local:
                for file_ftp in files_ftp:
                    if file == file_ftp:
                        print(f"Transferindo")
                        ftp.storbinary(f"STOR {file}", open(f"{local_dir}/{file}", "rb"))
                        files_transferidas.append(file)
            print(f'Foram atualizados {len(files_transferidas)}')
        else:
            print(f"O diretorio atual não é {str(os.getenv('TARGET_DIR'))}")
            
        for files_trnsf in files_transferidas:
            print(f"\nArquivo transferido: {files_trnsf}")
    
    def ftp_transfer(self, ftp, local_dir, target_dir, current__ftp_dir):
        if not os.path.exists(local_dir):
            print("Diretório local não encontrado, alterar o diretório local em .env")
            return

        # Check if already inside the desired directory
        current__ftp_dir = ftp.pwd()
        
        if current__ftp_dir == target_dir:
            # Transfer files
            self.transfer_files(ftp, local_dir, current__ftp_dir)
        else:
            print(f"Voce esta no diretório {current__ftp_dir}")
            print(f"Entrando no diretório {target_dir}")
            
            # Change to the desired directory
            ftp.cwd(target_dir)
            
            #Show current__ftp_dir
            print(f"Voce está no diretório {ftp.pwd()}")
            
            #Print directory content
            self.list_files_ftp(ftp)
            
            # Transfer files
            current__ftp_dir = ftp.pwd()
            self.transfer_files(ftp, local_dir, current__ftp_dir)
            
        
        print("\nArquivos transferidos, encerrando o programa")
        # Change back to the previous directory
        ftp.cwd(current__ftp_dir)
            
    def update(self, ftp, local_dir=str(os.getenv('LOCAL_DIR')), target_dir=str(os.getenv('TARGET_DIR')), current__ftp_dir=str(os.getenv('TARGET_DIR'))):
        self.ftp_transfer(ftp, local_dir, target_dir, current__ftp_dir)
    
#Create an instance of the class
autoupdater = AutoUpdater(str(os.getenv('HOST')), str(os.getenv('USERNAME')), str(os.getenv('PASSWORD')))

ftp = autoupdater.connect_ftp()

if ftp:
    current__ftp_dir = ftp.pwd()
    autoupdater.update(ftp)
else:
    print("Falha ao conectar ao servidor FTP")