import pickle
from selenium import webdriver
from time import sleep
import requests


def download_img_from_link (
    img_name: str,
    img_url: str,
    url : str,
    f,
)-> bool:
    try:
        content = requests.get(img_url).content
        with open(f'{img_name}', 'wb') as f:
            f.write(content)
    except Exception as e:
        f.write(f'Error with download {url}: {e}')
        return False
    return True




def load_cookies(
    browser: webdriver.Chrome,
    cookies_file: str
):
    # # region 1. Open Facebook
    # browser.get("http://facebook.com")
    # # endregion

    # # region 2.Load cookie from file
    # with open(cookies_file, "rb") as f:
    #     cookies = pickle.load(f)

    # for cookie in cookies:
    #     browser.add_cookie(cookie)
    # # endregion

    # region 3. Refresh the browser
    browser.get("http://facebook.com")
    print(f'Sleep 60s to Log in Facebook ...')
    sleep(60)
    # endregion
    return browser