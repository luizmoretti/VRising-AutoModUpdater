from localdir import LocalDirChecker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import json
import re

class ThunderModsDownload:
    def __init__(self, driver, local_dir_return):
        self.driver = driver
        self.local_dir_return = local_dir_return
    
    def driveroptions():
        options = Options()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        #Set default download path
        options.add_experimental_option("prefs", { "download.default_directory": r"C:\Users\luiza\Desktop\Projetos\AutoModUpdate\temp" })
        return options
    
    def thunderdownload(self):
        
        with open ("json/mods.json", "r") as f:
            datajson = json.load(f)
            
        self.driver = webdriver.Chrome(options=ThunderModsDownload.driveroptions())
        
        for data in datajson:
            nome_arquivo = data['name']
            data_atualizacao = data['data']
            link_referencia = data['ref']
            atualizado = data['updated']
            versao = data['version']
            
            if atualizado == True:
                #Open single True condition in a diferent tab
                print(f'\nAtualizando módulo {nome_arquivo}')
                self.driver.get(link_referencia)
                time.sleep(1)
                
                #Find Version text and get version number using regex pattern
                version = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]')


                #Extract version number from text usin group 1
                version = version.text
                version = re.findall(r'\w+\-\w+\-(\d.+)', version)
                version = version[0]
                print(f"{version}\n")
                time.sleep(1)

                #wait until download button is clickable and click it
                download = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/a')))
                download.click()
                time.sleep(1)
                
                #Update infos in json file for the new infos, version, updated and current timestamp and make a copy of the json file
                #Create a copy of the json file
                with open ("json/mods.json", "w") as f:
                    datajson[nome_arquivo]['updated'] = False
                    datajson[nome_arquivo]['version'] = version
                    datajson[nome_arquivo]['data'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    json.dump(datajson, f, indent=4)
                
                # -------------------------------- Copy json file with new timestamp instruction ---------------------------#    
                #Make a copy of the json file in a new name with the current timestamp
                os.system(f'copy json/mods.json json/mods_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json')
                
                #Print name of the new json file that has been created
                print(f'json/mods_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json foi criado\n')
                time.sleep(1)
                # ------------------------------------------- End of instruction -------------------------------------------#
            
                #Print of the file that have been updated
                print(f"Arquivo {nome_arquivo} atualizado em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f'Módulo {nome_arquivo} foi ja foi atualizado em {data_atualizacao}')
                
                
            


#Initiate ThunderModsDownload
start = ThunderModsDownload
start.thunderdownload(self=start)
                        