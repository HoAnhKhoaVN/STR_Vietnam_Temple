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


# region Setting logging
# cur_time = datetime.now()
# str_cur_time = cur_time.strftime("%Y_%m_%d")

# os.makedirs('log', )
# logging.basicConfig(
#     filename=f'log/{str_cur_time}.log', level=logging.DEBUG,
#     format='[%(asctime)s: %(filename)s] - %(levelname)s - %(message)s',
#     encoding='utf-8'
# )
# endregion
 
# region handle ctrl + c
def handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == 'y':
        print("")
        exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)

# endregion

ROOT ='eval_img_click_next'
LOG_PATH = 'log'
TIME_OUT = 3600

def get_one_image(
    url : str,
    time_to_post : str,
    num: int,
    # cookies_file: str = 'cookie/my_cookie.pkl',
    root : str = ROOT
):
    def press_next_button(
        _id: str,
        driver = webdriver.Chrome,
    ):
        cont = 0
        url_before = driver.current_url
        url_current  = driver.current_url
        while url_before == url_current :
            print(f'Press next button {cont}')
            cont+=1

            if cont > 50:
                print(f'Reload {url_current} after {cont} attempts press next button!!!')
                driver.get(url_current)
                first_div = WebDriverWait(driver, timeout= TIME_OUT).until(
                    method= EC.presence_of_element_located(("tag name", "div"))
                )
                _id = first_div.get_attribute("id")
            next_xpath = '//*[@id="facebook"]/body'
            body_selector = driver.find_element(By.XPATH, next_xpath)
            body_selector.send_keys(Keys.ARROW_RIGHT)

            print(f'Wait until load new page!')
            sleep(3)
            url_current  = driver.current_url
        return driver, _id
        
    # region 1. Get web driver and open page
    print(f'1. Get web driver and open page')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--log-level=1') # https://stackoverflow.com/questions/66997942/error-with-permissions-policy-header-when-using-chromedriver-to-a-headless-br
    # options.page_load_strategy = 'eager'
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--start-maximized")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options= options)
    # driver = load_cookies(
    #     driver,
    #     cookies_file
    #     )
    # e = time()
    # print(f'Time to Get web driver and open page : {(e-s)} seconds')
    # endregion

    # region 2. Wait driver
    print(f'2. Wait driver')
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=TIME_OUT, poll_frequency=2, ignored_exceptions=errors)
    # endregion

    # region 3. Get get first tag div to get id
    print(f'3. Get get first tag div to get id')
    # s = time()
    driver.get(url)

    # first_div = driver.find_element("tag name", "div")
    first_div = wait.until(
        method= EC.presence_of_element_located(("tag name", "div"))
    )
    _id = first_div.get_attribute("id")
    # e = time()
    # print(f'Time to get first tag div to get id : {(e-s)} seconds')
    # print(f'_id = {_id}')
    # sleep(2) # Sleep for waiting load data
    # endregion

    # region 4. Get log file
    print(f'ROOT : {root}')
    if not os.path.exists(path = root):
        os.makedirs(root, exist_ok = True)

    print(f'4. Get log file')
    curr_log_fd = os.path.join(LOG_PATH, time_to_post)
    os.makedirs(
        name = curr_log_fd,
        exist_ok= True
    )
    # endregion

    # region 5. Main process
    s = time()
    signal.signal(signal.SIGINT, handler)
    print(f'5. Main process...')
    print(f'Time to post: {time_to_post}')
    with open(f'{curr_log_fd}/{time_to_post}_good.log', 'w') as f, \
        open(f'{curr_log_fd}/{time_to_post}_err.log', 'w') as ferr, \
        open(f'{curr_log_fd}/{time_to_post}_general.log', 'w') as fgen:

        iterator = 0
        while iterator < num:
            # region 5.1 : Get current url
            wait.until(
                method = EC.visibility_of()
            )
            curr_url = driver.current_url
            print(f'========= ITERATOR: {iterator} ==========')
            # print('5.1 : Get current url\n')
            # print(f'====> Current url: {curr_url}\n')
            fgen.write(f'========= ITERATOR: {iterator} ==========\n')
            # fgen.write('5.1 : Get current url\n')
            fgen.write(f'Current url: {curr_url}\n')
            # endregion

            # region 5.2: Ignore video
            # fgen.write('5.2: Ignore video\n')
            # print('5.2: Ignore video')
            if 'videos' in curr_url:
                fgen.write(f'URL: {curr_url} is a video\n')
                ferr.write(f'{curr_url}')
                driver, _id = press_next_button(
                    driver = driver,
                    _id = _id
                )

                # print(f'Sleep 30s to wait next photo')
                # sleep(30)
                continue
            # endregion

            # region 5.3 Get image
            # fgen.write(f'5.3 Get image\n')
            # print(f'5.3 Get image')
            # s = time()
            f.write(f'{curr_url}\n')
            print(f'Current URL: {curr_url}')
            xpath = f'//*[@id="{_id}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'

            
            is_exist_img_selector = wait.until(
                method= EC.element_attribute_to_include(
                    locator=(By.XPATH, xpath),
                    attribute_='src'
                )
            )
            if is_exist_img_selector:
                img_selector = driver.find_element(By.XPATH, xpath)
                link_full_img = img_selector.get_attribute('src')
            else:
                break

            # e = time()
            # print(f'Time to Get image : {(e-s)} seconds')

            # endregion
              
            # region 5.4 Download image    
            img_name = link_full_img.split('/')[-1].split('?')[0]
            img_path = os.path.join(
                root,
                img_name
            )
            fgen.write(f'Download image: {img_path}\n')
            # s = time()
            is_success = download_img_from_link(
                img_path,
                link_full_img,
                curr_url,
                fgen
            )
            # e = time()
            # print(f'Time to Download image : {(e-s)} seconds')


            if is_success:
                fgen.write('===>Success download image\n')
                # print('***Success download image***')
                iterator+=1
            else:
                fgen.write('==>Error download image!!!\n')
                # print('Error download image!!!')
            # endregion

            driver, _id = press_next_button(
                _id = _id, 
                driver= driver
            )
    # endregion
    e = time()
    print(f'Time to download {num} image : {(e-s)} seconds')
    print(f'Average time per image: {(e-s)/num}')

    driver.close()
    print(f'Check {curr_log_fd}')

def crawl_images_multi_process(
    args : tuple
):
    return get_one_image(
        url = args[0],
        time_to_post= args[1],
        num= args[2],
        root= args[3],
    )

def muti_process():
    frames = [
        # Thread 1
        (
            'https://www.facebook.com/100017529549025/videos/g.1087253598032345/674759979784981',
            '23_06_2020_demo_MP',
            5,
            ROOT
        ),
        # Thread 2
        (
            'https://www.facebook.com/photo/?fbid=763172220766864&set=g.1087253598032345',
            '15_08_2019_demo_MP',
            7,
            ROOT
        ),

    ]
    threads = [Thread(target=crawl_images_multi_process, args=(frame,)) for frame in frames]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == '__main__':
    # region Input
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-url",
        "--url",
        required=True,
        help="URL post with image"
    )

    ap.add_argument(
        "-ttp",
        "--time_to_post",
        required=True,
        help="Time to post image"
    )

    ap.add_argument(
        "-r",
        "--root_dir",
        required=True,
        help="Root directory for save image."
    )

    ap.add_argument(
        "-n",
        "--num",
        required=True,
        help="Number of images to crawl"
    )
    args = ap.parse_args()
    # endregion

    # region main process
    get_one_image(
        url= args.url,
        time_to_post= args.time_to_post,
        root= args.root_dir,
        num= int(args.num)
    )
    # endregion



    
    # region I
    # get_one_image(
    #     url='https://www.facebook.com/photo/?fbid=158402785294766&set=g.1087253598032345',
    #     time_to_post='test_new_print',
    #     root= 'test_new_print',
    #     num=10
    # )
    # endregion

    # # region II
    # get_one_image(
    #     url='https://www.facebook.com/photo/?fbid=416116868846358&set=g.1087253598032345',
    #     time_to_post='22_02_2018',
    #     root= ROOT,
    #     num=2000
    # )
    # # endregion

    # # region III
    # get_one_image(
    #     url='https://www.facebook.com/photo/?fbid=2578580975517812&set=g.1087253598032345',
    #     time_to_post='18_12_2018',
    #     root= ROOT,
    #     num= 2000
    # )
    # # endregion

    # # region IV
    # get_one_image(
    #     url='https://www.facebook.com/photo/?fbid=681512902703683&set=g.1087253598032345',
    #     time_to_post='06_06_2020',
    #     root= ROOT,
    #     num=2000
    # )
    # # endregion