import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

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

    sleep(10)

    pickle.dump(browser.get_cookies(), open("my_cookie.pkl","wb"))

    browser.close()