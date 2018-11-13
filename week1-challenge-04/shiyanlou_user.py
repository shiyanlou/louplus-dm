import requests
from lxml import html


def user_info(user_id):

    url = "https://www.shiyanlou.com/user/{}/".format(user_id)
    content = requests.get(url)

    if content.status_code == 200:
        tree = html.fromstring(content.text)
        user_name = tree.xpath('//span[@class="username"]/text()')[0]
        user_level = tree.xpath('//span[@class="user-level"]/text()')[0][1:]
        join_date = tree.xpath('//span[@class="join-date"]/text()')[0][:10]
        return user_name, int(user_level), join_date
    else:
        user_name, user_level, join_date = (None, None, None)
        return user_name, user_level, join_date


