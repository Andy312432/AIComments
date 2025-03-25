from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle
import json
import time
import keyboard


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

#login
driver.get("http://www.facebook.com/")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

link = "https://www.facebook.com/bwbg.tw?locale=zh_TW"
driver.get(link)  
#driver.implicitly_wait(3)

#login window
try:
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div").click()
except:
    pass

tmp = ""
#find comment button
while(1):

    time.sleep(1)
    #scroll page
    scrollElement = driver.find_element(By.XPATH, "//html")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 950;",scrollElement)
    

    #find comment button
    posts = driver.find_elements(By.XPATH, "//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs xkrqix3 x1sur9pj' and contains(text(), '留言')]/parent::span/parent::div")
    for element in posts:
        try:
            # 等待元素可點擊
            element.click()
            print("成功點擊留言按鈕")
            break
        except Exception:
            print("無法點擊，繼續嘗試下一個")
    time.sleep(1)

    post_time = BeautifulSoup(driver.page_source, "lxml").find(class_="html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 xdt5ytf x1iyjqo2 x1n2onr6 xqbnct6 xga75y6").find(class_="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j").get_text()

    #check if post is the same
    if(post_time == tmp):
        print("post is the same")
        #close post
        driver.find_element(By.XPATH, "//div[@aria-label='關閉']").click()
        continue

    tmp = post_time


    #scroll page
    scrollElement = driver.find_element(By.XPATH, "//div[contains(@class,'xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m')]")
    driver.execute_script('arguments[0].scrollTop = 1000;', scrollElement)

    
    time.sleep(1)
    #all comments
    driver.find_element(By.XPATH, "//span[contains(text(), '最相關')]").click()
    driver.find_element(By.XPATH,"//span[contains(text(), '包含可能是垃圾訊息')]").click()#FIXME

    print("scrolling")
    tmp2 = 0
    while True:
        tmp2 += 1
        try:
            for i in driver.find_elements(By.XPATH, "//span[contains(string(.), '查看') and contains(string(.), '則回覆')]/parent::*"):
                i.click()
            for i in driver.find_elements(By.XPATH, "//span[contains(text(), '已回覆')]"):
                i.click()
        except:
            pass
        
        # 每30次滾動檢查一次是否到底
        if tmp2 % 8 == 0:
            time.sleep(1)
            # 檢查是否已經滾動到底部
            if driver.execute_script("return arguments[0].scrollHeight", scrollElement) <= driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight", scrollElement):
                print("已經滾動到底部")
                break  # 跳出 while 迴圈
            else:
                continue  # 進行下一次滾動
        
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollElement)
        time.sleep(1/2) 

    time.sleep(1/10)
    soup = BeautifulSoup(driver.page_source, "lxml")
    post_block = soup.find(class_="html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 xdt5ytf x1iyjqo2 x1n2onr6 xqbnct6 xga75y6")
    comments_block_all = post_block.find(class_="html-div x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp")
    comment_blocks = comments_block_all.find_all(class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi")

    toDump = []
    toDump.append(post_time)
    for comment_block in comment_blocks:
            
            comment = comment_block.find(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u") 
            commentTime = comment_block.find(class_ = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xi81zsa x1s688f")
            if(comment == None or comment.get_text() == ""):
                continue
            toDump.append([comment.get_text(), commentTime.get_text()])

    #存入json
    with open('comments.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(toDump, indent=2, ensure_ascii=False))
        f.write(",\n")
        print("儲存成功")
    
    #close post
    driver.find_element(By.XPATH, "//div[@aria-label='關閉']").click()

driver.close()