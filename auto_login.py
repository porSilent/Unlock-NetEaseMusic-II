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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B68CAEA73F1E9292D870A9A749C32113CF38E7329B35BD7281FCBA137DA0AB284D1CBEE33DDCCF2E1AB3E81AD118A137B40D7030E3617E15A81B2EC7845B6BB374A201A91F39D4443EA07F83986F3951BDB0F4565578C3B3EA9A72756E4B5BBD57256739E53DF98424C14E27426E9B782019D797604C94AEC3A35D53724816FC87559F9A9284B8DDAE549AB3865CFC1C607EF609C4D48D3648A4C73253E7CEB6F1B7E65203EBC0F91DEFE7E5472A5A91D701BF184EB35C087027CB3A696EB7E92E9F59A1A01A7DDCEAA894E84203B8ECFE4D801563D247C7B1F8585908B65E4639AF6A024D0CBCB1C4B6DDFF526D6CAF304BE4B3D148F038051482A8A95E4D7A1D63B0A21027DC923C6597B6D4960FBF7A37581A6024F5A061A37615F59FB285AA58763E8C68F883CF2D5B188BC48047AFD9578C3A1AF3BDCAA13879820CB92EC76FE3A220F527FB03F838A469C8D6A2A81D9E49631123B20AAC38C3EB590CC5"})
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
