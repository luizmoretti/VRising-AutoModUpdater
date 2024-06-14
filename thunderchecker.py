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

        def format_date(moddata):
            now = datetime.datetime.now()
            time_mapping = {
                "a day ago": now - datetime.timedelta(days=1),
                "1 minute ago": now - datetime.timedelta(minutes=1),
                "a minute ago": now - datetime.timedelta(minutes=1),
                "an hour ago": now - datetime.timedelta(hours=1),
                "a week ago": now - datetime.timedelta(weeks=1),
                "a year ago": now - datetime.timedelta(weeks=52)
            }
            for key, value in time_mapping.items():
                if moddata == f"Last updated: {key}":
                    return value.strftime("%Y-%m-%d")

            minutes_match = re.match(r"Last updated: (\d+) minutes ago", moddata)
            if minutes_match:
                minutes = int(minutes_match.group(1))
                return (now - datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%d")

            hours_match = re.match(r"Last updated: (\d+) hours ago", moddata)
            if hours_match:
                hours = int(hours_match.group(1))
                return (now - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d")

            days_match = re.match(r"Last updated: (\d+) days ago", moddata)
            if days_match:
                days = int(days_match.group(1))
                return (now - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

            weeks_match = re.match(r"Last updated: (\d+) weeks ago", moddata)
            if weeks_match:
                weeks = int(weeks_match.group(1))
                return (now - datetime.timedelta(weeks=weeks)).strftime("%Y-%m-%d")

            months_match = re.match(r"Last updated: (\d+) months ago", moddata)
            if months_match:
                months = int(months_match.group(1))
                return (now - datetime.timedelta(weeks=months*4)).strftime("%Y-%m-%d")

            return moddata
        
        if maincardmenu is not None:
            cards = maincardmenu.find_elements(By.CSS_SELECTOR, ".mb-2")
            for card in cards:
                # Get name and lastrelease
                name_element = card.find_element(By.TAG_NAME, "h5")
                updatedata_element = card.find_element(By.TAG_NAME, "small")
                href_element = card.find_element(By.CSS_SELECTOR, "a")

                modname = name_element.text.strip()
                moddata = updatedata_element.text.strip()
                modref = href_element.get_attribute("href")

                formated_date = format_date(moddata)

                # Check for spaces in the name
                formatedname = modname.replace(" ", "") if " " in modname else modname

                if formated_date and formatedname:
                    mod_info = {
                        "name": f"{formatedname}.dll",
                        "data": formated_date,
                        "ref": modref,
                        "updated": False,
                        "version": "0.0.0"
                    }
                    self.mods_infos.append(mod_info)

            # Save the updated mods information to the JSON file
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




#Create a istance of the class
start = ThunderModsChekerUpdate(webdriver.Chrome(options=options), {})

#Method Caller
start.thunderchecker()