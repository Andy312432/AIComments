# Facebook留言爬蟲 - 支援多年份抓取
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import time
import random
import keyboard

# 設定起始與結束年份
start_year = 2020
end_year = 2020

# 啟動瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 登入 Facebook（使用 cookie）
driver.get("http://www.facebook.com/")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# 開啟目標粉專
link = "https://www.facebook.com/bwbg.tw?locale=zh_TW"
driver.get(link)

# 關閉登入視窗（若有）
try:
    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div")
    login_button.click()
except:
    pass

# 工具函式
def wait_for_element(xpath, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return None

def click_if_clickable(elements, retries=3):
    for _ in range(retries):
        for element in elements:
            try:
                element.click()
                return True
            except:
                continue
        time.sleep(1)
    return False

def check_if_bottom(scroll_element):
    time.sleep(1.5)
    scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)
    scroll_top = driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight", scroll_element)
    return scroll_height <= scroll_top

# 開始迴圈跑每一年
for year in range(start_year, end_year + 1):
    print(f"=== 開始抓取 {year} 年 ===")

    # 開啟篩選條件
    try:
        driver.find_element(By.XPATH, "//div[@aria-label='篩選條件' or @aria-label='Filters']").click()
        wait_for_element("//div[@aria-label='選擇年分下拉式功能表']").click()
        driver.find_element(By.XPATH, f"//span[text()='{year}年']/parent::*/parent::*").click()
        click_if_clickable(driver.find_elements(By.XPATH, "//div[@aria-label='完成' and @role='button']"))
        time.sleep(2)
    except Exception as e:
        print(f"無法切換年份 {year}：{e}")
        continue

    first_comment_tmp = ""
    retry = 0

    while True:
        scroll_element = driver.find_element(By.XPATH, "//html")
        driver.execute_script("arguments[0].scrollTop += 960;", scroll_element)
        time.sleep(random.uniform(0.5, 1.2))

        posts = driver.find_elements(By.XPATH, "//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs xkrqix3 x1sur9pj' and contains(text(), '留言')]/parent::span/parent::div")

        for element in posts:
            if '1 則留言' not in element.text:
                try:
                    element.click()
                    retry = 0
                    break
                except:
                    if posts.index(element) == len(posts) - 1:
                        retry += 1
                        break
                    continue
            else:
                retry = 0
                continue

        if retry >= 1:
            if retry >= 20:
                driver.execute_script("arguments[0].scrollTop += 1100;", scroll_element)
            continue

        wait_for_element("//div[contains(@class, 'xga75y6')]", timeout=10)
        soup = BeautifulSoup(driver.page_source, "lxml")
        post_block = soup.find("div", class_="html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 xdt5ytf x1iyjqo2 x1n2onr6 xqbnct6 xga75y6")
        if not post_block:
            continue

        post_time_elem = post_block.find("span", class_="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j")
        post_time = post_time_elem.get_text() if post_time_elem else ""

        '''
        if str(year) not in post_time:
            print(f"跳過非 {year} 貼文：{post_time}")
            continue'
        '''

        scroll_element = driver.find_element(By.XPATH, "//div[contains(@class,'xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m')]")
        driver.execute_script("arguments[0].scrollTop += 100;", scroll_element)
        wait_for_element("//span[contains(text(), '最相關')]").click()
        wait_for_element("//span[contains(text(), '包含可能是垃圾訊息')]").click()

        print("滾動留言區...")
        for _ in range(9999):
            if check_if_bottom(scroll_element):
                break
            if keyboard.is_pressed('Esc'):
                break
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_element)
            time.sleep(random.uniform(0.1, 0.3))

        soup = BeautifulSoup(driver.page_source, "lxml")
        post_block = soup.find("div", class_="html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 xdt5ytf x1iyjqo2 x1n2onr6 xqbnct6 xga75y6")
        comments_block_all = post_block.find("div", class_="html-div x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp") if post_block else None
        comment_blocks = comments_block_all.find_all("div", class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi") if comments_block_all else []

        rows = []
        for idx, comment_block in enumerate(comment_blocks):
            comment = comment_block.find(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")
            if not comment:
                continue
            comment_time = comment_block.find("span", class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee")
            if idx == 0:
                if first_comment_tmp == comment.get_text():
                    retry += 1
                    print("第一則留言與前一則相同，跳過...")
                    break
                else:
                    first_comment_tmp = comment.get_text()
                rows.append([post_time, comment.get_text(strip=True), comment_time.get_text() if comment_time else ""])
            else:
                rows.append(["", comment.get_text(strip=True), comment_time.get_text() if comment_time else ""])

        pd.DataFrame(rows).to_csv(f'comments_{year}.csv', mode='a', index=False, header=False, encoding='utf-8')
        print(f"{len(rows)} 則留言已加入 comments_{year}.csv")

        click_if_clickable(driver.find_elements(By.XPATH, "//div[@aria-label='關閉']"))

        if(retry>0):
            scroll_element = driver.find_element(By.XPATH, "//html")
            driver.execute_script("arguments[0].scrollTop += 300;", scroll_element)
            retry = 0

print("✅ 所有年份留言抓取完成！")
driver.quit()
