import os
import json
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException




try :
    Cookies = os.environ.get('COOKIES')
    sckey = os.environ.get('KEY')
except Exception as e:
    title = f'FYS checkin'
    over_time = datetime.datetime.now()
    sendContent = f'FYS信息导入失败:' + over_time.strftime("%Y-%m-%d %H:%M:%S")
    sckey = '008c265cf0d846489be11e6e565d5285'
    plusurl = f"http://www.pushplus.plus/send?token={sckey}&title={title}&content={sendContent}"


try :
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options) # 打开浏览器
    browser.set_page_load_timeout(3) # 设置超时时间
    try:
        browser.get('https://bbs.fyscs.com/member.php?mod=logging&action=login') # 打开登录页
    except TimeoutException: # 捕获超时异常
        print("超时跳过")


    # 注入cookie
    listCookies = json.loads(Cookies)

    for cookie in listCookies: 
        if isinstance(cookie.get('expiry'), float):
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)

    # 打开登录界面
    browser.get('https://bbs.fyscs.com/plugin.php?id=dsu_paulsign:sign') # 打开签到页
except Exception as e:
    print("打开网页失败")
    title = f'FYS checkin'
    over_time = datetime.datetime.now()
    sendContent = f'FYS网站打开失败:' + over_time.strftime("%Y-%m-%d %H:%M:%S")
    sckey = '008c265cf0d846489be11e6e565d5285'
    plusurl = f"http://www.pushplus.plus/send?token={sckey}&title={title}&content={sendContent}"

try :
    # 选择心情
    browser.find_element(by=By.XPATH, value='//*[@id="wl"]').click()
    # 选择填写文字
    browser.find_element(by=By.XPATH, value='//*[@id="todaysay"]').send_keys('email_adr')
    # 点击签到
    browser.find_element(by=By.XPATH, value='//*[@id="qiandao"]/table[1]/tbody/tr/td/div/a/img').click()
    browser.get('https://bbs.fyscs.com/plugin.php?id=dsu_paulsign:sign') # 打开签到页
    regData = browser.find_element(by=By.XPATH, value='//*[@id="ct"]/div[1]/p[3]/font').text
    over_time = datetime.datetime.now()
    over_time.strftime("%Y-%m-%d")
    if (over_time.strftime("%Y-%m-%d") in regData):
        print("签到成功")
        title = f'FYS checkin'
        over_time = datetime.datetime.now()
        sendContent = f'FYS签到成功:' + over_time.strftime("%Y-%m-%d %H:%M:%S")
        sckey = '008c265cf0d846489be11e6e565d5285'
        plusurl = f"http://www.pushplus.plus/send?token={sckey}&title={title}&content={sendContent}"
        if (requests.get(plusurl).status_code == 200):
            print("推送成功")
    else:
        print("签到失败")
except Exception as e:
    regData = browser.find_element(by=By.XPATH, value='//*[@id="ct"]/div[1]/p[3]/font').text
    over_time = datetime.datetime.now()
    over_time.strftime("%Y-%m-%d")
    if (over_time.strftime("%Y-%m-%d") in regData):
        print("已签到")
        title = f'FYS checkin'
        over_time = datetime.datetime.now()
        sendContent = f'FYS已经签到成功:' + over_time.strftime("%Y-%m-%d %H:%M:%S")
        sckey = '008c265cf0d846489be11e6e565d5285'
        plusurl = f"http://www.pushplus.plus/send?token={sckey}&title={title}&content={sendContent}"
        if (requests.get(plusurl).status_code == 200):
            print("推送成功")




