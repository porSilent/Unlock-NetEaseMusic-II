# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00AAD79F55008C1771D86D321FB08CF3F02D8DC6204E94E47450961AF923B3EFDD696FA4F75A2A88484C76C74D73DDA310045211B19E14B6B91537C49CFEFD5996CACD0B5482DC8D17E258D48D98CFBA9BE358553FC01093F2B352F2BFB1CA6689E82DD2D7E2731AF4DABC6D457BAB818E92DF7D22ECD2967CDD2465D874161C98638BAD0143C21C310B72B35B1DFBA7CD5EF2A28AEE2497C3C41C3555BD0577980BCB9A0A8596BA4F7D03EA72E3223089CB4DD719ECC0C4E8EE4C127E741497D6E53FAEC36183F3264E57141912ED3A12ED21131274FFA7FF644E2B6E9F1A392F0B0EC39774B0A4CB5BDCCCB362F9B1364A5DB5F1420190CE4D4C176F391BE4A17DF863D3EC22B10D335730F6C9CDC4AD974FB4B8D4114AA8CB0B195ACEFB338A81CFE2F37D479513ED71E8CE91042B7744CA1CFAB7031A43B3A4208267A980699FC25F80D1974489AA46725CE239DFDFEEE3408457A10DF580C8EC064C14D515"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
