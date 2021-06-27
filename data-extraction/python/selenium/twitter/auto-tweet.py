from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from pathlib import Path
import os

USERNAME_OR_EMAIL = ''
PASSWORD = ''

opts = Options()
opts.set_headless()

driver = Firefox(
    options=opts,
    executable_path=os.path.join(Path().resolve().parent, 'geckodriver-v0.29.1-win64', 'geckodriver.exe')
)

driver.get('https://twitter.com/login')

username_or_email = driver.find_element_by_name('session[username_or_email]')
username_or_email.clear()
username_or_email.send_keys(USERNAME_OR_EMAIL)

password = driver.find_element_by_name('session[password]')
password.clear()
password.send_keys(PASSWORD)

driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()

new_tweet_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']")
    )
)

new_tweet_button.click()

active_element = driver.switch_to.active_element
active_element.send_keys('This is my Selenium Tweet')

driver.find_element_by_xpath('//div[@data-testid="tweetButton"]').click()

sleep(5)
driver.quit()

login_check = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//span[@class="_2BMnTatQ5gjKGK5OWROgaG"]')
    )
)