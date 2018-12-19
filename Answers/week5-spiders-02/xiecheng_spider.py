# 使用 BeautifulSoup 进行解析
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.common.proxy import Proxy, ProxyType


'''
dstation: 出发城市代码
astation: 到达城市代码
date: 出发日期，形如 2018-10-30
driver: 创建的 webdriver
'''
def get_ticket_info(dstation, astation, date, driver):
    url = "http://flights.ctrip.com/booking/%s-%s-day-1.html?DDate1=%s" % (
        dstation, astation, date)
    # 一直尝试到成功
    while True:
        try:
            driver.get(url)
            break
        except TimeoutException as e:
            pass
    # 等待页面加载出来
    time.sleep(2)

    # webdriver 执行 js 语句滑动窗口，一直滑动到底部
    initial_pagesource = driver.page_source
    while True:
        # 滑到页面底部，暂停 0.1 秒是为了等待页面刷新出结果
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # 等待数据加载
        time.sleep(1)
        # 如果当前页面和上一个页面的 html 内容不同，则表明滑动到底部了
        if initial_pagesource == driver.page_source:
            break
        initial_pagesource = driver.page_source

    # 使用 BeautifulSoup 解析 html 内容
    soup = BeautifulSoup(initial_pagesource)
    # 获取搜索结果的每一个项
    result = soup.find_all("div", class_=["search_table_header", ])
    result_list = []
    for ticket_info in result:
        try:
            # 航空公司名、出发时间、到达时间
            company_name, start_time, arrival_time = [
                x.text for x in ticket_info.find_all('strong')]
            # 出发机场、到达机场
            start_airport, arrival_airport = [
                x.text for x in ticket_info.find_all("div", class_=["airport", ])]
            tmp = [x.text for x in ticket_info.find_all(
                "span", class_=["direction_black_border", ])]
            # 飞机类型，准点率（可能没有）
            if len(tmp) == 2:
                airpane_type, ontime_rate = tmp
                ontime_rate = float(''.join(filter(str.isdigit, ontime_rate)))/100
            else:
                airpane_type = tmp[0]
                ontime_rate = 0
            # 航班编号
            airpane_number = [x.text for x in ticket_info.find_all("span")][2]
            # 价格(经济舱)
            price = int([''.join(list(filter(str.isdigit, x.text)))
                         for x in ticket_info.find_all("span", class_=["base_price02", ])][0])
            result_list.append([company_name, start_time, arrival_time, start_airport,
                                arrival_airport, airpane_type, ontime_rate, airpane_number, price])

        except Exception as E:
            print(E)

    # 按机票价格排序后返回
    return sorted(result_list, key=lambda x: x[-1])

if __name__ == "__main__":
    # driver = webdriver.PhantomJS(executable_path="./chromedriver", service_args=['--load-images=no'])
    options = Options()
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
    # driver = webdriver.Chrome("./chromedriver")
    result_list = get_ticket_info('CTU', 'SHA', '2018-10-30', driver)
    print(result_list)