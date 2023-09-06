
from bs4 import BeautifulSoup
from lxml import etree

def get_element_from_idx(
    idx
)-> str:
    return dom.xpath(f'//*[@id="mount_0_0_Z0"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[{idx}]/div/div/div/a')[0].values()[-3]

if __name__ == '__main__':
    url = 'demo_src_page.html'
    with open(url, 'r', encoding='utf-8') as f:
        html_content=f.read()
    soup = BeautifulSoup(html_content, "lxml")
    dom = etree.HTML(str(soup))
    c = 0
    with open('test_load_img_link_2.txt', 'w') as f:
        while True:
            c+=1
            try:
                link_post = f'https://www.facebook.com{get_element_from_idx(c)}'
                print(f'{link_post}')
                f.write(f'{link_post}\n')
            except Exception as e:
                print(f"Error: {e}")
                break

    print(f'Length of image: {c-1}')

    # print(dir(dom.xpath('//*[@id="mount_0_0_Z0"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div[2000]/div/div/div/a')[0].values))
    