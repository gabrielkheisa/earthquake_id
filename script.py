import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import base64
import json
import urllib.parse

from selenium.webdriver.chrome.options import Options

key = "API_KEY" 

while(1):
    try:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        
        # To bypass CloudFlare's detection
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        
        # To bypass CloudFlare's detection
        # options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'user-agent={user_agent}')
        
        browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options) 
        
        '''
        if the popup appear, use this xpath
        /html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[2]
        else, use the original one
        /html/body/div[1]/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[2]
        '''
        

        browser.delete_all_cookies()
        browser.get("https://www.bmkg.go.id/gempabumi/gempabumi-realtime.bmkg")

        browser.implicitly_wait(10)
        
        browser.save_screenshot('screen_shot_gempa.png')   

        

        #Quick copy
        #browser.find_element_by_xpath("").get_attribute('') 

        news = {
            "server_update": dt_string,
            "news": [
              {
                "time": browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[2]").get_attribute('textContent'), 
                "lat":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[3]").get_attribute('textContent'),
                "lon":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[4]").get_attribute('textContent'),
                "mag":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[5]").get_attribute('textContent'),
                "dep":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[6]").get_attribute('textContent'),
                "reg":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[7]").get_attribute('textContent')
              }
            ]
        }
        
        i = 2
        
        while(i<150):
            news["news"].append(
                {
                    "time": browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[2]").get_attribute('textContent'), 
                    "lat":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[3]").get_attribute('textContent'),
                    "lon":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[4]").get_attribute('textContent'),
                    "mag":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[5]").get_attribute('textContent'),
                    "dep":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[6]").get_attribute('textContent'),
                    "reg":  browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/table/tbody/tr["+str(i)+"]/td[7]").get_attribute('textContent')
                }
            )
            
            i = i + 1
            
        #news = json.dumps(news)
        
        with open('data_earthquake.json', 'w') as f:
            json.dump(news, f)
        
        !cp data_earthquake.json /var/www/api.dev.gabrielkheisa.xyz/earthquake_id/cache.txt

        browser.quit()
        print("Sleep for 15 minutes")
        time.sleep(15*60)
        
    except Exception as e:
        print(e)
        browser.quit()
        print("Sleep for 15 minutes")
        time.sleep(15*60)

