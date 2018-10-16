# -*- coding: utf-8 -*-

import requests
import os
import time
from bs4 import BeautifulSoup


def spider(item, text=True):

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/55.0.2883.75 Safari/537.36'

    headers = {
        'User-Agent': user_agent,
        'Referer': item,
    }

    response = requests.get(item, headers=headers, timeout=5)

    if text:
        return response.text

    else:
        # raw -> byte
        return response


def parse_html(item):

    result = []
    soup = BeautifulSoup(item, "lxml")
    img_list = soup.select(".BDE_Image")

    for img in img_list:

        result.append(img.attrs['src'])

    return result


def download(items, path):

    if not os.path.exists(path):
        os.mkdir(path)

    print("Total: %s" % len(items))

    for item in items:

        img = spider(item, text=False).content
        name = items.index(item)

        with open('%s/%s.jpg' % (path, name), 'wb') as f:
            f.write(img)
            f.close()

        print('%s: %s' % (items.index(item)+1, item))

        time.sleep(1)

    return True


def start():

    page_num = 1
    page_end = 3
    page_url = "http://tieba.baidu.com/p/2476521385?pn="
    base_dir = os.path.abspath('.')
    spider_log = os.path.join(base_dir, 'spider.log')
    crawled = open(spider_log, 'r').readlines()

    #
    for num in range(page_num, page_end + 1):

        sub_dir = os.path.join(base_dir, str(num))
        url = page_url + str(num)

        # crawled
        if url+'\n' in crawled:
            print('\033[0;31mThe %s is crawled, skipped !!\033[0m' % url)
            continue

        # process
        html_data = spider(url)
        pic_list = parse_html(html_data)
        status = download(pic_list, sub_dir)

        if status:
            with open(spider_log, 'a+') as F:
                F.write(url + '\n')
                F.close()

        else:
            print('Crawl " %s " is failed, please check it !!!' % url)
            break

        # sleep
        time.sleep(30)


if __name__ == '__main__':

    start()
