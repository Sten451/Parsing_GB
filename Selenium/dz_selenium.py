import json
import copy
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

url = "https://quotes.toscrape.com/login"
url2 = "https://quotes.toscrape.com/scroll"
service = Service('./geckodriver')
driver = webdriver.Firefox(service=service)
action = ActionChains(driver)

try:
    driver.get(url=url)
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_all_elements_located((By.ID, 'password')))
    username = driver.find_element(By.ID, 'username')
    username.send_keys("admin")
    password = driver.find_element(By.ID, 'password')
    password.send_keys("admin")
    action.send_keys(Keys.ENTER).perform()
    time.sleep(1)

    driver.get(url=url2)
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
    time.sleep(1)

    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    dictionary_final = []
    dictionary = {}
    for item in quotes:
        dictionary['text'] = (item.find_element(By.CLASS_NAME, 'text')).text
        dictionary['author'] = (
            item.find_element(By.CLASS_NAME, 'author')).text
        tags = item.find_elements(By.CLASS_NAME, 'tag')
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)
        dictionary['tags'] = tag_list
        dictionary_final.append(copy.deepcopy(dictionary))

    with open('final.json', 'w', encoding='utf-8') as file:
        parsing = json.dumps(dictionary_final, ensure_ascii=False)
        file.write(parsing)
    print("Парсер закончил работу...")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
