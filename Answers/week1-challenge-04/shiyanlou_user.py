import requests
from lxml import html


def user_info(user_id):

    url = "https://www.lanqiao.cn/users/{}/".format(user_id)
    content = requests.get(url)

    if content.status_code == 200:
        tree = html.fromstring(content.text)
        # 首先选取所以 div 元素，要求其 class 属性中包含 name 字段
        # 再取 div 下的 span
        user_name = tree.xpath("//div[contains(@class, 'name')]/span/text()")[0].strip()
        user_level = tree.xpath("//div[contains(@class, 'name')]/span/text()")[1].strip()[1:]
        return user_name, int(user_level)
    else:
        user_name, user_level = (None, None)
        return user_name, user_level