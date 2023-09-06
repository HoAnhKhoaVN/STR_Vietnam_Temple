import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime

if __name__ == "__main__":
    # 0. Declare the browser
    browser = webdriver.Chrome()

    # 1. Open faceboook
    browser.get("http://facebook.com")

    # 2. Truy to login

    txtUser = browser.find_element(by = By.XPATH, value= '//*[@id="email"]')
    txtUser.send_keys("0368367501")

    txtPassword = browser.find_element(by = By.XPATH, value= '//*[@id="pass"]')
    txtPassword.send_keys("Th@nhlongruotdokhonghot1999")

    txtPassword.send_keys(Keys.ENTER)

    sleep(20)

    # region get current time
    curr_time = datetime.now()
    str_curr_time = curr_time.strftime("%Y%m%d")
    # endregion 

    # region dump cookies
    save_path = f'cookie/f"cookie_{str_curr_time}.pkl'

    with open(save_path,"wb") as f:
        pickle.dump(
            obj= browser.get_cookies(),
            file= f
        )
    # endregion

    browser.close()