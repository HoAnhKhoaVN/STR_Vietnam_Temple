from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import wget
from os import makedirs
import requests
from PIL import Image
import pickle

def init_chrome():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless') # Open tab chrome
    return chrome_options

def load_cookies(
    browser: webdriver.Chrome
):
    # 1. open Facebook
    browser.get("http://facebook.com")

    # 2.Load cookie from file
    cookies = pickle.load(open("my_cookie.pkl","rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    # 3. Refresh the browser
    browser.get("http://facebook.com")

    print(f'Sleep 60s to Log in Facebook ...')
    sleep(60)
    return browser

def main():
    # region 1. Login
    driver = webdriver.Chrome()
    driver = load_cookies(driver)
    driver.get(f"https://www.facebook.com/groups/1087253598032345/media/photos")
    # div = driver.find_element(by = B)
    # print(f'div : {div}')

    # endregion
    # print(f'drive: {driver}')

    print(f'You have 30s to change class-name')
    sleep(15)

    # region Scroll down to get all photos
    # thanks https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python/43299513#43299513
    SCROLL_PAUSE_TIME = 3
    while True:

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling 
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait 10 seconds before reload the page

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(f'new height: {new_height}')
            print(f'last height: {last_height}')

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

    # endregion

    with open('page_source_v2.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    # exit(0)
    print(f'Starting download image')

    # region Get all link image
    c = 0
    link_posts = []
    with open('test_load_img_link_2.txt', 'w') as f:
        while True:
            c+=1
            try:
                img_mes = driver.find_element(By.XPATH, f'//*[@id="mount_0_0_MM"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[{c}]/div/div/div/a')
                link_post = img_mes.get_attribute(name ='href')
                print(f'{link_post}')
                f.write(f'{link_post}\n')
            except Exception as e:
                print(f"Error: {e}")
                break
            # link_posts.append(link_post)
            # print(f'Link: {link_post}')
    # endregion 
    print(f'Starting download ...')
    # //*[@id="mount_0_0_MM"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[469]/div/div/div/a/img
    # //*[@id="mount_0_0_MM"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/a

    # region do something
    sleep(360)
    # endregion
    



    

    # Find all the image elements on the page.
    # ID = 523
    # xpath_photo_thumnail = f'//*[@id="mount_0_0_SW"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[{ID}]/div/div/div/a'
    # photo_thumnail = driver.find_elements(By.XPATH, xpath_photo_thumnail)

    # Loop through the image elements and download each image.
    # for image_element in image_elements:
    #     image_url = image_element.get_attribute("src")
    #     image_name = image_url.split("/")[-1]
    #     makedirs(name = 'HAN_NOM', exist_ok= True)
    #     wget.download(image_url, f"HAN_NOM/{image_name}")

    # Close the ChromeDriver.
    driver.close()





def download_img_from_link (
    img_name: str,
    img_url: str,
    url : str
):
    content = requests.get(img_url).content
    with open(f'{img_name}', 'wb') as f:
        # Storing the image data inside the data variable to the file
        f.write(content)
    
if __name__ == "__main__":
    # GROUP_ID = '1087253598032345'
    main()
    IMG_XPATH = '//*[@id="mount_0_0_Xw"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'
    NEXT_XPATH = '//*[@id="mount_0_0_Xw"]/div/div[1]/div/div[1]'
#     image_url ='https://scontent.fsgn2-5.fna.fbcdn.net/v/t39.30808-6/363397285_1349852849221683_5118187527205202762_n.jpg?stp=cp6_dst-jpg&_nc_cat=104&ccb=1-7&_nc_sid=5cd70e&_nc_ohc=7UJhlJ3cPtoAX9POgId&_nc_ht=scontent.fsgn2-5.fna&oh=00_AfDj_Wvm31Tuj8plVS86idyOfsXDlQvAtwwtlsSVINsOlw&oe=64EE0CB4'
#     download_img_from_link(
#         img_name= 'demo',
#         img_url=image_url
#     )
# //*[@id="mount_0_0_SW"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[265]/div/div/div/a

# //*[@id="mount_0_0_SW"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[252]/div/div/div/a

# //*[@id="mount_0_0_fy"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[146]/div/div/div/a