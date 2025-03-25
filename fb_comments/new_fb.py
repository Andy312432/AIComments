from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

links = ["https://www.facebook.com/share/p/1Qqjg1nvdL/",
"https://www.facebook.com/share/v/18iSgt5wP5/",
"https://www.facebook.com/share/p/1DaEyvqEP3/",
"https://www.facebook.com/share/p/1A6q223gW5/",
"https://www.facebook.com/share/p/1AFkarzz3o/",
"https://www.facebook.com/share/p/15neYa9zQ7/",
"https://www.facebook.com/share/p/1B4Mdp94j7/",
"https://www.facebook.com/share/p/1ALjbfpjfc/",
"https://www.facebook.com/share/p/16EJqPPhv5/",
"https://www.facebook.com/share/p/16K5sr2Wps/",
"https://www.facebook.com/share/p/1A8RzvYPRx/",
"https://www.facebook.com/share/p/15yBsrrFq6/",
"https://www.facebook.com/share/p/18ddG392iG/",
"https://www.facebook.com/share/p/15q8i55Kf9/",
"https://www.facebook.com/share/p/159mRSAFHL/",
"https://www.facebook.com/share/p/15wNoSsxVp/",
"https://www.facebook.com/share/p/1W4dSMy3VS/",
"https://www.facebook.com/share/p/15oKCVGHb9/",
"https://www.facebook.com/share/p/1CFUp2RxQe/",
"https://www.facebook.com/share/p/1KhT68ZFLg/",
"https://www.facebook.com/share/p/16E1EhfUpj/",
"https://www.facebook.com/share/p/1BNSa2BTvK/",
"https://www.facebook.com/share/p/14wfSs3asb/",
"https://www.facebook.com/share/p/1D1gYGvK9R/",
"https://www.facebook.com/share/p/1AN55XEJEZ/",
"https://www.facebook.com/share/p/1Bs9CBeoyw/",
"https://www.facebook.com/share/p/16FTjZsUGa/",
"https://www.facebook.com/share/p/15bGqv38vT/",
"https://www.facebook.com/share/p/1Kd43etd4b/",
"https://www.facebook.com/share/p/1BjhAKqmNK/",
"https://www.facebook.com/share/p/15sBmHP6jK/",
"https://www.facebook.com/share/p/1APB98zDkd/",
"https://www.facebook.com/share/p/15vK2Jcwj2/",
"https://www.facebook.com/share/p/1BPt8WtHps/",
"https://www.facebook.com/share/p/1E9FYRahyB/",
"https://www.facebook.com/share/p/1B6WF5xNSz/",
"https://www.facebook.com/share/p/18i6B11f9G/",
"https://www.facebook.com/share/p/1BaBq7z5sw/",
"https://www.facebook.com/share/p/19zSac9xrJ/",
"https://www.facebook.com/share/p/1BCzYjZUvt/",
"https://www.facebook.com/share/p/18wtutnRgA/",
"https://www.facebook.com/share/p/1DpGUbtGvN/",
"https://www.facebook.com/share/p/165J8Jg241/",
"https://www.facebook.com/share/p/18eqApQEPG/",
"https://www.facebook.com/share/p/15uZ7Uyai7/",
"https://www.facebook.com/share/v/1NDbsUbrkY/",
"https://www.facebook.com/share/p/15mzmLi37H/",
"https://www.facebook.com/share/p/1AXQmPx6PU/"]

linkNumOffset = 1
for linkNUM in range(len(links)-linkNumOffset):

    driver.get(links[linkNUM+linkNumOffset])  
    #driver.implicitly_wait(3)
    if "/v/" in links[linkNUM+linkNumOffset]:
        #login
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div").click()
        #all comments
        driver.find_element(By.XPATH, "//span[contains(text(), '最相關')]").click()
        driver.find_element(By.XPATH,"//span[contains(text(), '包含可能是垃圾訊息')]").click()#FIXME

        time.sleep(1)
        scrollElement = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div[2]")
        driver.execute_script('arguments[0].scrollTop = 2000;', scrollElement)
        #expand
        driver.find_element(By.XPATH, "//span[contains(text(), '查看更多留言')]").click()
    else:
        scrollElement = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]")   
        driver.execute_script('arguments[0].scrollTop = 2000;', scrollElement) 

        #all
        driver.find_element(By.XPATH, "//span[contains(text(), '最相關')]").click()
        driver.find_element(By.XPATH,"//span[contains(text(), '包含可能是垃圾訊息')]").click()#FIXME
    

    time.sleep(2)
    tmp = 0
    while(1):
        tmp += 1
        try:
            for i in driver.find_elements(By.XPATH, "//div[contains(text(), '查看更多')]"):
                i.click()
            for i in driver.find_elements(By.XPATH, "//span[contains(text(), '已回覆')]"):
                i.click()
                pass
        except:
            pass
        if tmp == 50:
            if(input('con?') == " "):
                break
            else:
                tmp = 0
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;",scrollElement)
        time.sleep(1/100)


    soup = BeautifulSoup(driver.page_source, "lxml") 
    comments_block = soup.find_all(class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi")
    
    toDump = []
    for comment_block in comments_block:
            
            comment = comment_block.find(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u") 
            commentTime = comment_block.find(class_ = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xi81zsa x1s688f")
            if(comment == None):
                continue
            toDump.append([comment.get_text(), commentTime.get_text()])
            print([comment.get_text(), commentTime.get_text()])

    #存入json
    f = open(f'result_{linkNUM+linkNumOffset}.json', 'w', encoding='utf-8') #json
    json.dump(toDump, f, indent=2, sort_keys=True, ensure_ascii=False)
    f.close()


driver.close()