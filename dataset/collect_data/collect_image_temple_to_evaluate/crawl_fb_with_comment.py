import argparse
from time import sleep, time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from crawl_fb_utils import load_cookies, download_img_from_link
from threading import Thread
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import logging
from datetime import datetime
import os
import signal
import readchar
from pickle import load, dump



if __name__ == "__main__":
    TIME_OUT = 3600
    url = 'https://www.facebook.com/groups/1087253598032345/permalink/1634021823355517/'
    LOG_PATH = 'log_crawl_with_comment'
    time_to_post = "04_01_2018"

    # region 1. Get web driver and open page
    print(f'1. Get web driver and open page')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options= options)
    # endregion

    # region 2. Wait driver
    print(f'2. Wait driver')
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=TIME_OUT, poll_frequency=2, ignored_exceptions=errors)
    # endregion

    # region 3. Get log file
    # print(f'3. Get log file')
    # curr_log_fd = os.path.join(LOG_PATH, time_to_post)
    # os.makedirs(
    #     name = curr_log_fd,
    #     exist_ok= True
    # )
    # endregion

    # region 4. Loging FB
    print(f'4. Log FB')
    # 1. Open faceboook
    driver.get("http://facebook.com")

    # 2. Truy to login

    txtUser = driver.find_element(by = By.XPATH, value= '//*[@id="email"]')
    txtUser.send_keys("0368367501")

    txtPassword = driver.find_element(by = By.XPATH, value= '//*[@id="pass"]')
    txtPassword.send_keys("Th@nhlongruotdokhonghot1999")

    txtPassword.send_keys(Keys.ENTER)
    sleep(5)
    # endregion

    # region load page
    print(f'Load page')
    driver.get(url)
    print(f'Sleep 20s to wait load page!!!')
    sleep(20)
    # endregion

    # region get poster
    # poster_xpath = '//*[@id=":r17:"]/div/div/span/div'
    # poster_selector = driver.find_element(by=By.XPATH, value= poster_xpath)
    # div_selector= poster_selector.find_elements('tag name', 'div')
    # poster_text = '\n'.join(div_.text for div_ in div_selector)
    # print(f'Poster_text: {poster_text}')
    # endregion

    # region get first div
    first_div = wait.until(
        method= EC.presence_of_element_located(("tag name", "div"))
    )
    _id = first_div.get_attribute("id")

    # endregion

    # sleep(360)
    # region get comments
    comment_xpath = f'//*[@id="{_id}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[2]/ul'
    print(f'comment_xpath: {comment_xpath}')
    comment_selector = wait.until(
        method= EC.presence_of_element_located((By.XPATH, comment_xpath))
    )
    # comment_selector = driver.find_element(by=By.XPATH, value= comment_xpath)
    div_selector= comment_selector.find_elements('tag name', 'div')
    comment_text = [div_.text for div_ in div_selector]
    with open('comment_text.plk', 'wb') as f:
        dump(comment_text, f)
    print(f'Poster_text: {comment_text}')

    sleep(360)
    # endregion
    driver.close()




