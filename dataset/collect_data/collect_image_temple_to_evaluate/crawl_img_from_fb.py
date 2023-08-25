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
    return browser


def main():
    # Set up the ChromeDriver and navigate to the Facebook group page.
    # chrome_options = init_chrome()

    # region Get Accessibility to Facebook


    # endregion


    driver = webdriver.Chrome()
    driver.get(f"https://www.facebook.com/groups/1087253598032345/media/photos")
    # driver.get(f"https://www.selenium.dev/")

    # Find all the image elements on the page.
    ID = 523
    xpath_photo_thumnail = f'//*[@id="mount_0_0_SW"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[{ID}]/div/div/div/a'
    photo_thumnail = driver.find_elements(By.XPATH, xpath_photo_thumnail)


    print(f'image_elements : {photo_thumnail}')

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
):
    content = requests.get(img_url).content
    with open(f'{img_name}.png', 'wb') as f:
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