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
driver = webdriver.Chrome(service=Service(r'd:\chromedriver.exe'))
driver.implicitly_wait(10)

driver.get('https://tianjin.anjuke.com/community/')
time.sleep(10)  # 等待页面加载
driver.maximize_window()

# 指定文件名
filename = 'ajk.csv'
# 创建CSV写入器
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入标题行
    writer.writerow(['地区', '小区', '价格', '标签', '地址', '总户数', '竣工时间', '所属商圈', '停车位', '物业费', '停车费'])

# 爬取页数
page_number = 1
#爬取地区数

try:
    for r in range(2, 22):
        s_r=str(r)
        xpa = '//*[@id="__layout"]/div/section/section[2]/div[1]/section/div/ul/li[' + s_r + ']/a'
        region = driver.find_element(By.XPATH, xpa)
        area = region.text.strip()
        region.click()
        time.sleep(1)

        # 循环直到没有下一页
        while True:
            print(f'正在爬取第{r-1}个区，第 {page_number} 页...')
            # 等待页面加载完成
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".li-row")))
            # 找到所有的租房信息容器
            rent_info_list_elements = driver.find_elements(By.CSS_SELECTOR, ".li-row")
            # 存储当前页的租房信息
            page_rent_info_list = []
            # 遍历租房信息容器，提取信息
            p = 1
            for rent_info in rent_info_list_elements:
                title = rent_info.find_element(By.CSS_SELECTOR, ".li-title").text.strip()
                price = rent_info.find_element(By.CSS_SELECTOR, ".community-price").text.strip() + '元/平方米'
                tags = [span.text.strip() for span in rent_info.find_elements(By.CSS_SELECTOR, "span.prop-tag")]
                address = rent_info.find_element(By.XPATH, "/html/body/div[1]/div/div/section/section[3]/section/div[2]/a[16]/div[2]/div[2]/span[3]").text.strip()


                q=str(p)
                xp = "/html/body/div[1]/div/div/section/section[3]/section/div[2]/a["+q+"]/div[2]/div[1]/div"
                rent_info.find_element(By.XPATH,xp).click()
                time.sleep(1)
                num = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div[1]").text.strip()
                time_done = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[1]").text.strip()
                com = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[10]/div[2]/div[1]").text.strip()
                park = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[13]/div[2]/div[1]").text.strip()
                fee = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[14]/div[2]/div[1]").text.strip()
                park_fee = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[15]/div[2]").text.strip()
                driver.back()


                # 将提取的信息存储为字典
                rent_info_dict = {
                    '地区': area,
                    '标题': title,
                    '价格': price,
                    '标签': " ".join(tags),
                    '地址': address,
                    '户数': num,
                    '竣工时间': time_done,
                    '所属商圈': com,
                    '停车位': park,
                    '物业费': fee,
                    '停车费': park_fee
                }
                print(rent_info_dict)
                page_rent_info_list.append(rent_info_dict)
                p+=1


            # 将当前页的数据写入文件
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for rent_info in page_rent_info_list:
                    writer.writerow([
                        area,
                        rent_info['标题'],
                        rent_info['价格'],
                        rent_info['标签'],
                        rent_info['地址'],
                        rent_info['户数'],
                        rent_info['竣工时间'],
                        rent_info['所属商圈'],
                        rent_info['停车位'],
                        rent_info['物业费'],
                        rent_info['停车费']
                    ])
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
