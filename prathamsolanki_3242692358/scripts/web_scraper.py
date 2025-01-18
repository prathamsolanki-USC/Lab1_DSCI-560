from selenium import webdriver
import time
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


destination_file_path = '/home/prathamuser/Desktop/prathamsolanki_3242692358/data/raw_data/web_data.html'
gecko_driver_path = '/snap/bin/firefox.geckodriver'


options = Options()
#options.add_argument("--headless")  
#options.add_argument("--disable-gpu") 
options.add_argument("--window-size=1920,1080")


service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get("https://www.cnbc.com/world/?region=world")
    
    driver.implicitly_wait(20)  
    time.sleep(10)
    html_content = driver.page_source
    html_parsed = BeautifulSoup(html_content,'html.parser')

    with open(destination_file_path, "w", encoding="utf-8") as file:
        file.write(html_parsed.prettify())
    print("Successfully written HTML contents of CNBC home page to web_data.html")
finally:

    driver.quit()
