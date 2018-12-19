import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import re
import sqlite3
import pandas as pd

'''
爬虫代码分为三步:
1. 爬取房屋 id
2. 根据房屋 id 组合 url，然后依次爬取房屋的具体界面获取信息
3. 保存到本地
'''

base_url = 'https://sh.lianjia.com/zufang/'
test_url = 'https://sh.lianjia.com/zufang/pg1/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

# 获取一页的房屋列表，具体为房屋的 id，例如 107100610451
def getHouseURLList(page_url):
    try:
        r = requests.get(page_url, timeout=5, headers=headers)
        if r.status_code==403:
        	print('访问被拒，请稍后再试')
    except requests.exceptions.Timeout:
        # 请求超时，返回无效数据
        return None
    content = r.content
    soup = BeautifulSoup(content)
    result_list = list(soup.select('#house-lst')[0].children)
    return_list = []
    for result in result_list:
        return_list.append(result['data-id'])
    return return_list

# 示例
# return_list = getHouseURLList(test_url)

# 房屋 id
data_id_list = []

# 多走几轮，以获得更全的数据
for _ in range(1):
    # for i in tqdm(range(1, 101)):
    for i in tqdm(range(1, 2)):
        page_url = base_url+'pg{}/'.format(i)
        return_list = getHouseURLList(page_url)
        if not return_list:
            time.sleep(10)
            continue
        data_id_list.extend(return_list)

# 去除重复数据
data_id_list = list(set(data_id_list))

# 写入本地文件，保存房屋 id
with open('house_id_list.txt', 'w') as f:
    f.write('\n'.join(data_id_list))


# 清理面积
def clean_str(s):
    # 去除中文
    re.sub(r'[^\x00-\x7f]', '', s)
    new_s = []
    for c in s:
        # 遇到非数字则舍去
        if c.isdigit(): new_s.append(c)
        else: break
    return ''.join(new_s)

# 定义一个类保存数据
class Room(object):
    def __init__(self, url):
        self.done = False
        self.area = 0
        self.url = url
        self.price = ''
        self.isRemoved = ''
        self.special_label = ''
        self.title = ''
        self.floor = ''
        self.is_near_subway = ''
        self.publish_time = ''
        self.rooms = ''
        self.toilet = ''
        self.halls = ''
        self.rent_way = ''
        self.location = ''

    # 房屋面积
    def setArea(self, area):
        self.area = float(clean_str(area))

    # 价格
    def setPrice(self, price):
        self.price = price

    # 是否下架
    def setIsRemoved(self, isRemoved):
        self.isRemoved = isRemoved

    # 是否精装修
    def setSpecialLabel(self, special_label):
        self.special_label = special_label

    # 户型: 房间数量，房间，大厅，卫生间; 出租方式: 整租、合租
    def setType(self, type):
        tmp = type.split()
        if len(tmp) == 1:
            room_count = tmp[0]
            rent_way = '暂无信息'
        else:
            room_count, rent_way = tmp
        room_count = re.sub(r'[^\x00-\x7f]', ' ', room_count).strip().split()
        room_count = list(map(int, room_count))

        # 部分房屋无卫生间或客厅
        if len(room_count) < 3:
            for i in range(3 - len(room_count)):
                room_count.append(0)

        self.rooms = room_count[0]
        self.halls = room_count[1]
        self.toilet = room_count[2]
        self.rent_way = rent_way

    # 位置
    def setLocation(self, location):
        self.location = location

    # 是否靠近地铁
    def setSubway(self, is_near_subway):
        self.is_near_subway = is_near_subway

    # 朝向
    def setDirection(self, direction):
        self.direction = direction

    # 楼层
    def setFloor(self, floor):
        self.floor = floor

    # 发布时间
    def setPublishTime(self, publish_time):
        self.publish_time = publish_time

    # 房屋标题
    def setTitle(self, title):
        self.title = title

    # 房屋链接
    def setURL(self, URL):
        self.url = URL

    # 是否爬取成功
    def setDone(self, done):
        self.done = done

    def __repr__(self):
        return str(self.__dict__)

# 给定 url 获取房屋信息
def getRoom(url):
    room = Room(url)
    try:
        r = requests.get(url, timeout=5, headers=headers)
        if r.status_code==403:
        	print('访问被拒，请稍后再试')
    except requests.exceptions.Timeout:
        time.sleep(2)
        print('timeout')
        return Room('invalid')
    content = r.content.decode()

    soup = BeautifulSoup(content, features='lxml')

    title = soup.find('h1', class_='main').text
    room.setTitle(title)

    price_div = soup.find('div', class_='price')
    price_list = list(price_div.stripped_strings) # ['9000', '元/月', '精装修']
    price = ''.join(price_list[:2])
    room.setPrice(price)

    special_label = ' '.join(price_list[2:]) if len(price_list)>2 else '无'
    room.setSpecialLabel(special_label)
    isRemoved = '已下架' if price_div['class'][1] == 'isRemove' else '正在出租'
    room.setIsRemoved(isRemoved)

    room_info = soup.find('div', class_='zf-room')
    room_info_list = list(room_info.stripped_strings)

    location = "{} {} {}".format(room_info_list[15], room_info_list[16], room_info_list[11])
    room.setLocation(location)
    room.setPublishTime(room_info_list[-1])
    room.setArea(room_info_list[1])
    room.setType(room_info_list[3]) # 4室2厅3卫;
    room.setFloor(room_info_list[5])
    room.setDirection(room_info_list[7])
    room.setSubway(room_info_list[9])

    room.setDone(True)

    return room

# 连接数据库
conn = sqlite3.connect('lianjia.db')

cursor = conn.cursor()
# 创建表，如果已创建，则删除下面这行
cursor.execute('''
CREATE TABLE ROOM(
  url VARCHAR(1000) PRIMARY KEY,
  price Double,
  area Double,
  isRemoved VARCHAR(1000),
  special_label VARCHAR(1000),
  rooms INT,
  halls INT,
  toilet INT,
  rent_way INT,
  location VARCHAR(1000),
  is_near_subway VARCHAR(1000),
  direction VARCHAR(1000),
  floor VARCHAR(1000),
  publish_time VARCHAR(1000),
  title VARCHAR(1000)
)
''')

SELECT_COMMAND = "select * from ROOM where url='{}';"
INSERT_COMMAND = "insert into ROOM(url, price, area, isRemoved, \
                        special_label, rooms, halls, toilet, rent_way, \
                        location, is_near_subway, direction, floor, publish_time, title) \
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

# 根据上面爬取到的房屋 ID 组合生成 url，然后依次爬取
def getAllHouseInfo(file_path):
    base_url = 'https://sh.lianjia.com/zufang/{}.html'
    with open(file_path) as f:
        lines = f.readlines()

    urls = [base_url.format(line.strip('\n')) for line in lines]
    for url in tqdm(urls):
        cursor = conn.cursor()
        cursor.execute(SELECT_COMMAND.format(url))
        if len(cursor.fetchall()) != 0:
            continue
        cursor.close()
        # 如果失败，最多尝试 5 次
        count = 0
        while count < 5:
            room = getRoom(url)
            if room.done:
                break
            count += 1
        if count == 5:
            continue

        # 插入数据库
        cursor = conn.cursor()
        cursor.execute(INSERT_COMMAND,
                           (room.url, room.price, room.area, room.isRemoved, room.special_label,
                            room.rooms, room.halls, room.toilet, room.rent_way, room.location, room.is_near_subway,
                            room.direction, room.floor, room.publish_time, room.title))
        cursor.close()
        conn.commit()
        if cursor.rowcount != 1:
            print('插入错误')


getAllHouseInfo('house_id_list.txt')

csv_path = 'lianjia.csv'

cursor = conn.cursor()

# 保存到本地 csv 文件
cursor.execute('SELECT * FROM ROOM')

data = cursor.fetchall()
data = list(map(list, data))
name_attribute = ['url', 'price', 'area', 'state', 'label', 'rooms', 'halls', 'toilets', 'rentway', 'location',
                 'subway', 'direction', 'floor', 'publishtime', 'title']
data_frame =pd.DataFrame(columns=name_attribute,data=data)
data_frame.to_csv(csv_path, encoding='utf_8_sig')
conn.close()