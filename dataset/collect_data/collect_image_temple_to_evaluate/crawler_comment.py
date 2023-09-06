from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from time import sleep

def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("error write line")
    return data

def writeFileTxt(fileName, content):
    with open(fileName, 'a') as f1:
        f1.write(content + os.linesep)

def initDriver():
    # CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('disable-infobars')
    # chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    # chrome_options.add_argument("--verbose")
    # chrome_options.add_argument("--no-default-browser-check")
    # chrome_options.add_argument("--ignore-ssl-errors")
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    # chrome_options.add_argument("--no-first-run")
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-translate")
    # chrome_options.add_argument("--ignore-certificate-error-spki-list")
    # chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # prefs = {"profile.default_content_setting_values.notifications": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    # chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # chrome_options.add_argument('disable-infobars')

    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    return driver

def checkLiveClone(
    driver : webdriver.Chrome
    ):
    try:
        driver.get("https://mbasic.facebook.com/")
        sleep(2)
        driver.get("https://mbasic.facebook.com/")
        sleep(1)
        elementLive = driver.find_element(by = By.XPATH, value= '//a[contains(@href, "/messages/")]')
        if elementLive:
            print("Live")
            return True

        return False
    except Exception as e:
        print(f"Error: {e}")
        print("Check Live Fail")


def convertToCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except:
        print("Error Convert Cookie")


def checkLiveCookie(driver, cookie):
    try:
        driver.get('https://mbasic.facebook.com/')
        sleep(1)
        driver.get('https://mbasic.facebook.com/')
        sleep(2)
        loginFacebookByCookie(driver ,cookie)

        return checkLiveClone(driver)
    except Exception as e:
        print(f'Error: {e}')
        print("check live fail")


def loginFacebookByCookie(
    driver: webdriver.Chrome,
    cookie: str
    ):
    try:
        cookie = convertToCookie(cookie)
        print(cookie)
        if (cookie != None):
            script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
            driver.execute_script(script)
            sleep(5)
    except:
        print("loi login")

def outCookie(driver: webdriver.Chrome):
    try:
        sleep(1)
        script = "javascript:void(function(){ function deleteAllCookiesFromCurrentDomain() { var cookies = document.cookie.split(\"; \"); for (var c = 0; c < cookies.length; c++) { var d = window.location.hostname.split(\".\"); while (d.length > 0) { var cookieBase = encodeURIComponent(cookies[c].split(\";\")[0].split(\"=\")[0]) + '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path='; var p = location.pathname.split('/'); document.cookie = cookieBase + '/'; while (p.length > 0) { document.cookie = cookieBase + p.join('/'); p.pop(); }; d.shift(); } } } deleteAllCookiesFromCurrentDomain(); location.href = 'https://mbasic.facebook.com'; })();"
        driver.execute_script(script)
    except:
        print("loi login")


def getContentComment(driver: webdriver.Chrome):
    try:
        links = driver.find_element(By.XPATH, '//a[contains(@href, "comment/replies")]')
        ids = []
        if (len(links)):
            for link in links:
                takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
                textCommentElement = driver.find_element(By.XPATH, ('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                if (takeLink not in ids):
                    print(textCommentElement.text)
                    writeFileTxt('comments.csv', textCommentElement.text)
                    ids.append(takeLink)
        return ids
    except:
        print("error get link")

def getAmountOfComments(
    driver: webdriver.Chrome,
    postId: str,
    numberCommentTake: int
    ):
    try:
        driver.get("https://mbasic.facebook.com/" + str(postId))
        sumLinks = getContentComment(driver)
        while(len(sumLinks) < numberCommentTake):
            try:
                nextBtn = driver.find_element(By.XPATH, '//*[contains(@id,"see_next")]/a')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sumLinks.extend(getContentComment(driver))
                else:
                    break
            except:
                print('Error when cralw content comment')
    except:
        print("Error get cmt")

def getPostIds(
    driver: webdriver.Chrome,
    filePath: str = 'posts.csv'
    )-> None:

    allPosts = readData(filePath)
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = driver.find_elements(By.XPATH, '//a[contains(@href, "/sharer.php")]')
    if (shareBtn):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            if postId not in allPosts:
                print(postId)
                writeFileTxt(filePath, postId)

def getnumOfPostFanpage(
    driver: webdriver.Chrome,
    pageId: str,
    amount,
    filePath = 'posts.csv'
    )-> None:
    driver.get("https://touch.facebook.com/" + pageId)
    while len(readData(filePath)) < amount:
        getPostIds(driver, filePath)


cookie = 'sb=CwLKZDVd57xk2zjacBD-Pj45; datr=CwLKZMU8Goo4bATeoMrJQsJv; c_user=100013813777659; m_page_voice=100013813777659; m_pixel_ratio=1; xs=25%3Aije2AFzHJ0IpoQ%3A2%3A1693337103%3A-1%3A6168%3A%3AAcWvWSDoaETDst4_UOns71HVCp8ZkNUQyn2QuUGqfA; wd=2560x1297; x-referer=eyJyIjoiL3Bob3RvLnBocD9mYmlkPTgxOTUzNDMyOTgyMDA2NSZpZD0xMDAwNTI5MDUxNzEyMzYmc2V0PWdtLjY2MDA0MTU1MDY3MTYwOTkmZWF2PUFmYm85QUpZQ2ZuS3Mzb011TGtYWVlTZmJXemRwNmhXQmpaeDZKd29jVWtsV0YzZHR3UG8tSmJmdnpVNW1WeXdYNncmcGFpcHY9MCZzb3VyY2U9NDgiLCJoIjoiL3Bob3RvLnBocD9mYmlkPTgxOTUzNDMyOTgyMDA2NSZpZD0xMDAwNTI5MDUxNzEyMzYmc2V0PWdtLjY2MDA0MTU1MDY3MTYwOTkmZWF2PUFmYm85QUpZQ2ZuS3Mzb011TGtYWVlTZmJXemRwNmhXQmpaeDZKd29jVWtsV0YzZHR3UG8tSmJmdnpVNW1WeXdYNncmcGFpcHY9MCZzb3VyY2U9NDgiLCJzIjoibSJ9; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1693434350185%2C%22v%22%3A1%7D; fr=0NfKOGzI58YnpFevz.AWWXI0XRMT5a41DnjZzb9aXWngQ.Bk77_R.XI.AAA.0.0.Bk78Iq.AWU8NA_BDro'
driver = initDriver()
isLive = checkLiveCookie(driver, cookie)
if (isLive):
    getnumOfPostFanpage(driver, '1087253598032345', 10, '1087253598032345.csv')
    for postId in readData('1087253598032345.csv'):
        getAmountOfComments(driver, postId, 1000)
