from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import json


#future url https://thunderstore.io/c/v-rising/p/deca/Bloodstone/versions/


#Options for headless mode
options = Options()
#options.add_argument("--headless")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--headless=new")

class ThunderModsChekerUpdate:
    def __init__(self, driver, mods_infos):
        self.driver = driver
        self.mods_infos = mods_infos
        
    def thunderchecker(self):
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://thunderstore.io/c/v-rising/')
        self.mods_infos = []
        
        maincardmenu = self.driver.find_element(By.CSS_SELECTOR,".package-list")

        if maincardmenu is not None:
            cards = maincardmenu.find_elements(By.CSS_SELECTOR,".mb-2")
            for card in cards:
                #Get name and lastrelease
                names = card.find_elements(By.TAG_NAME, "h5")
                updatedata = card.find_elements(By.TAG_NAME, "small")
                hrefmod = card.find_elements(By.XPATH, f"/html/body/div[2]/div[3]/div[2]/div[4]/div[{cards.index(card)+1}]/div[1]/a")

                for name in names:
                    for data in updatedata:
                        for ref in hrefmod:
                            modname = name.text
                            moddata = data.text
                            modref = ref.get_attribute("href")     
                            
                            formated_date = None
                            if moddata == "Last updated: a day ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 1 minute ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: a minute ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 2 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=2)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 3 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=3)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 4 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=4)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 5 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 6 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=6)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 7 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=7)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 8 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=8)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 9 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=9)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 10 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 11 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=11)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 12 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=12)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 13 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=13)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 14 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=14)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 15 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 16 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=16)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 17 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=17)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 18 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=18)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 19 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=19)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 20 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 21 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=21)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 22 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=22)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 23 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=23)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 24 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=24)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 25 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=25)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 26 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=26)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 27 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=27)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 28 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=28)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 29 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=29)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 30 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 31 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=31)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 32 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=32)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 33 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=33)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 34 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=34)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 35 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=35)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 36 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=36)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 37 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=37)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 38 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=38)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 39 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=39)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 40 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=40)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 41 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=41)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 42 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=42)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 43 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=43)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 44 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=44)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 45 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=45)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 46 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=46)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 47 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=47)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 48 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=48)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 49 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=49)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 50 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=50)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 51 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=51)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 52 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=52)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 53 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=53)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 54 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=54)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 55 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=55)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 56 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=56)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 57 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=57)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 58 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=58)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: 59 minutes ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(minutes=59)).strftime("%Y-%m-%d")
                            elif moddata == f"Last updated: an hour ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 2 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 3 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 4 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 5 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=5)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 6 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 7 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=7)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 8 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 9 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=9)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 10 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=10)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 11 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=11)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 12 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 13 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=13)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 14 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=14)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 15 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=15)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 16 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=16)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 17 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=17)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 18 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=18)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 19 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=19)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 20 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=20)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 21 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=21)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 22 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=22)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 23 hours ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(hours=23)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 2 days ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 3 days ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 4 days ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 5 days ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 6 days ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: a week ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 2 weeks ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(weeks=2)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 3 weeks ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: 2 months ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(weeks=8)).strftime("%Y-%m-%d")
                            elif moddata == "Last updated: a year ago":
                                formated_date = (datetime.datetime.now() - datetime.timedelta(weeks=52)).strftime("%Y-%m-%d")
                            else:
                                formated_date = moddata
                            
                            #Check for spaces in the name
                            if " " in modname:
                                formatedname = modname.replace(" ", "")
                            else:
                                formatedname = modname
                            
                            
                            if formated_date and formatedname:
                                self.mods_infos.append({
                                    "name": f"{formatedname}"+".dll",
                                    "data": formated_date,
                                    "ref": modref,
                                    "updated": False,
                                    "version": "0.0.0"
                                })
                                with open("json/mods.json", "w") as f:
                                    json.dump(self.mods_infos, f, indent=4)
                            
            #How many cards are there?
            total_cards = len(cards)
            print(total_cards)
        else:
            print("No cards menu found")
        time.sleep(2)
        self.driver.quit()
        
        #Make the function return True when finishe executing
        return False

#Export the class as a module using the name "ThunderCheker" and using the export function
__all__ = ["thunderchecker"]



#Create a istance of the class
start = ThunderModsChekerUpdate(webdriver.Chrome(options=options), {})

#Method Caller
start.thunderchecker()