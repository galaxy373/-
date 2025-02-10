import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


'''
# 配置Chrome选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
'''

# 初始化浏览器
driver = webdriver.Chrome(service=Service(r'd:\chromedriver.exe'))         #, options=options
driver.implicitly_wait(10)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
             """
})

driver.get('https://tianjin.anjuke.com/community/')
driver.maximize_window()
time.sleep(6)  # 等待页面加载

# 指定文件名
filename = 'ajk.csv'
# 创建CSV写入器
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入标题行
    writer.writerow(['小区', '价格', '标签' ,'总户数'])

# 爬取页数
page_number = 1
#总共页数
all_pages = 2
try:
    while page_number < all_pages+1:
        print(f'正在爬取第 {page_number} 页...')
        # 等待页面加载完成
        time.sleep(6)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".li-row")))
        # 找到所有的租房信息容器
        rent_info_list_elements = driver.find_elements(By.CSS_SELECTOR, ".li-row")
        # 存储当前页的租房信息
        page_rent_info_list = []
        # 遍历租房信息容器，提取信息
        for rent_info in rent_info_list_elements:
            title = rent_info.find_element(By.CSS_SELECTOR, ".li-title").text.strip()
            print (title)
            price = rent_info.find_element(By.CSS_SELECTOR, ".community-price").text.strip() + '元/月'
            tags = [span.text.strip() for span in rent_info.find_elements(By.CSS_SELECTOR, "span.prop-tag")]
            # mainWindow变量保存当前窗口的句柄
            mainWindow = driver.current_window_handle
            button = rent_info.find_element(By.XPATH, "/html/body/div[1]/div/div/section/section[3]/section/div[2]/a[@*]/div[2]/div[1]/div")
            button.click()
            time.sleep(3)
            nowWindow = driver.current_window_handle
            driver.switch_to.window(nowWindow)
            num = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div[1]").text.strip()
            print(num)
            driver.switch_to.window(mainWindow)
            driver.back()
            time.sleep(3)
            # 将提取的信息存储为字典
            rent_info_dict = {
                '标题': title,
                '价格': price,
                '标签': ", ".join(tags),
                '户数': num
            }
            page_rent_info_list.append(rent_info_dict)
        # 将当前页的数据写入文件
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for rent_info in page_rent_info_list:
                writer.writerow([rent_info['标题'],rent_info['价格'],rent_info['标签'],rent_info['户数']])
        # 寻找下一页按钮并点击
        next_page_button = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/section/section[3]/section/div[3]/a[2]")
        if not next_page_button:
            break
        next_page_button[0].click()
        # 设置随机间歇时间（例如：1到10秒之间的随机时间）
        time.sleep(random.uniform(1, 10))
        page_number += 1
except TimeoutException:
    print("页面加载超时")


finally:
    #关闭浏览器
    driver.quit()
    print(f'数据已存储到 {filename}')