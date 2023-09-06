from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import wget
from os import makedirs
import requests
from PIL import Image
import pickle
from crawl_img_from_fb import load_cookies, download_img_from_link
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

ROOT ='eval_img_click_next'

def get_lst_url(
    url_path: str = 'test_load_img_link_2.txt'
):
    with open(url_path, 'r') as f:
        res = f.readlines()
    res = list(map(lambda x: x.strip(), res))

    return res

def get_image_from_lst_url(
    lst_url_path : str
):
    # region 1. Get driver
    driver = webdriver.Chrome()
    driver = load_cookies(driver)
    # endregion

    # region 2. Get list of URLs
    lst_url= get_lst_url(
        lst_url_path
    )
    # endregion
    # curr_time = datetime.now()
    # str_cur_time = curr_time.strftime("%Y%m%d_%H%M")

    for url in tqdm(lst_url[325:1441], desc = 'Process to download'):
        # # region Ignore video
        # if 'videos' in curr_url:
        #     # Press next button
        #     next_xpath = '//*[@id="facebook"]/body'
        #     driver.find_element(By.XPATH, next_xpath).send_keys(Keys.ARROW_RIGHT)
        #     sleep(2)
        # # endregion

        # # region Get url
        driver.get(url)
        sleep(2)
        # #endregion

        # region get image
        first_div = driver.find_element("tag name", "div")
        _id = first_div.get_attribute("id")



        # xpath = f'//*[@id="{_id}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'
        # img_selector = driver.find_element(By.XPATH, xpath)
        # region Loop to get image
        xpath = f'//*[@id="{_id}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'
        for i in range(5):
            sleep(2)
            try:
                img_selector = driver.find_element(By.XPATH, xpath)
            except:
                img_selector = None
            
            if img_selector is not None:
                break
            else:
                print(f'Try again with {url}')
        
        if i == 4: 
            # Press next button
            # next_xpath = '//*[@id="facebook"]/body'
            # driver.find_element(By.XPATH, next_xpath).send_keys(Keys.ARROW_RIGHT)
            continue
        # endregion 


        link_full_img = img_selector.get_attribute('src')
        img_name = link_full_img.split('/')[-1].split('?')[0]
        img_path = os.path.join(
            ROOT,
            img_name
        )
        # endregion

        # print(f'Link: {link_full_img}')
        # print(f'PATH: {img_path}')
        # print('-------------------')
        download_img_from_link(
            img_path,
            link_full_img
        )


        # next_xpath = '//*[@id="facebook"]/body'
        # driver.find_element(By.XPATH, next_xpath).send_keys(Keys.ARROW_RIGHT)
        # sleep(2)
    sleep(360)
    driver.close()
if __name__ == '__main__':
    get_image_from_lst_url(
        'test_load_img_link_2.txt'
    )