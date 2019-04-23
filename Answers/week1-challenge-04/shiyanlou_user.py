import requests
from lxml import html


def user_info(user_id):

    url = "https://www.shiyanlou.com/users/{}/".format(user_id)
    content = requests.get(url)

    if content.status_code == 200:
        tree = html.fromstring(content.text)
        user_name = tree.xpath(
            '//div[@class="user-meta"]/span/text()')[0].strip()
        user_level = tree.xpath(
            '//div[@class="user-meta"]/span/text()')[1].strip()[1:]
        join_date = tree.xpath(
            '//span[@class="user-join-date"]/text()')[0].strip()[:10]
        return user_name, int(user_level), join_date
    else:
        user_name, user_level, join_date = (None, None, None)
        return user_name, user_level, join_date
