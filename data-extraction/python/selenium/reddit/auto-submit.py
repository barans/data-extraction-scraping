from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from pathlib import Path
import os

USERNAME = ''
PASSWORD = ''


opts = Options()
opts.headless = False
opts.set_preference('dom.push.enabled', False)

driver = Firefox(
    options=opts,
    executable_path=os.path.join(Path().resolve().parent, 'geckodriver-v0.29.1-win64', 'geckodriver.exe')
)

driver.get('https://www.reddit.com/login/')


username = driver.find_element_by_name('username')
username.clear()
username.send_keys(USERNAME)

password = driver.find_element_by_name('password')
password.clear()
password.send_keys(PASSWORD)

driver.find_element_by_xpath('//button[@type="submit"]').click()

login_check = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//span[@class="_2BMnTatQ5gjKGK5OWROgaG"]')
    )
)

driver.get('https://www.reddit.com/r/selenium/submit')

title = driver.find_element_by_xpath("//textarea[@placeholder='Title']")
title.send_keys('Is Selenium good for Amazon Search Results?')

content = driver.find_element_by_xpath("//div[@role='textbox']")
content.send_keys('Has anyone used this as a Scraper? Did you have some troubles for CAPTCHAS or proxies etc?')

driver.find_element_by_xpath('//button[@class="_18Bo5Wuo3tMV-RDB8-kh8Z _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 "]').click()

sleep(5)
driver.quit()