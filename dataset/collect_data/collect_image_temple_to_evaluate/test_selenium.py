import pytest
from selenium import webdriver
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_fails(driver):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()

    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, 'box0')


def test_sleep(driver):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()

    time.sleep(2)
    added = driver.find_element(By.ID, "box0")

    assert added.get_dom_attribute('class') == "redbox"


def test_implicit(driver):
    driver.implicitly_wait(2)
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()

    added = driver.find_element(By.ID, "box0")

    assert added.get_dom_attribute('class') == "redbox"


def test_explicit(driver):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    revealed = driver.find_element(By.ID, "revealed")
    wait = WebDriverWait(driver, timeout=2)

    driver.find_element(By.ID, "reveal").click()
    wait.until(lambda d : revealed.is_displayed())

    revealed.send_keys("Displayed")
    assert revealed.get_property("value") == "Displayed"


def test_explicit_options(driver):
    # Get url
    s = time.time()
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    
    revealed = driver.find_element(By.ID, "revealed")
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)

    driver.find_element(By.ID, "reveal").click()
    wait.until(lambda d : revealed.send_keys("Displayed") or True)

    assert revealed.get_property("value") == "Displayed"

def test_explicit_wait_with_expected_condition():
    s = time.time()
    # import webdriver 
    from selenium import webdriver 
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    e = time.time()
    print(f'Time to import webdriver : {(e-s)} seconds')
    
    # create webdriver object
    s = time.time()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options= options)
    e = time.time()
    print(f'Time to import webdriver : {(e-s)} seconds')

        
    # get geeksforgeeks.org 
    s = time.time()
    driver.get("https://www.geeksforgeeks.org/") 
    e = time.time()
    print(f'Time to get geeksforgeeks.org  : {(e-s)} seconds')
      
    # get element  after explicitly waiting for 10 seconds
    s = time.time()
    xpath = '//*[@id="RA-root"]/div/div[1]/div[1]/div[2]/span/span/span[1]/input'
    try:
        element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
    except TimeoutError:
        pass

    e = time.time()
    print(f'Time to get element : {(e-s)} seconds')

    # Send keys
    s = time.time()
    element.send_keys("Hello World")
    e = time.time()
    print(f'Time to Send keys : {(e-s)} seconds')

    time.sleep(60)
    driver.close()

if __name__ == "__main__":
    # test_explicit_options(webdriver.Chrome())
    test_explicit_wait_with_expected_condition()