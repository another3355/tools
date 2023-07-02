from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import urllib
import time
import getpass


import undetected_chromedriver as uc


def baseDriver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=114)
    driver.implicitly_wait(10)
    return driver


def download(url, save_dir):
    driver = baseDriver()

    driver.get(url)

    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    ele = driver.find_element(By.XPATH, '//*[@id="-"]/div[1]/div')
    source = ele.get_attribute("innerHTML")

    # # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(source, "html.parser")

    # 查找所有的图片标签
    img_tags = soup.find_all("img")

    print(len(img_tags))

    # 创建目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)

    # 遍历所有图片标签，并下载图片
    for index, img in enumerate(img_tags):
        # 获取图片的URL
        img_url = img["src"]
        file_name = f"avatar_{index}.jpg"  # 文件名
        save_path = os.path.join(save_dir, file_name)  # 图片保存路径
        opener = urllib.request.URLopener()
        opener.addheader(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        )
        try:
            opener.retrieve(img_url, save_path)
        except Exception as e:
            print(e)
        print("图片已下载：", img_url)

    print("头像下载完成！")


if __name__ == '__main__':
    url = "https://www.pexels.com/zh-cn/new-photos/"
    save_dir = f"/Users/{getpass.getuser()}/crypto/avatars"
    download(url, save_dir)
