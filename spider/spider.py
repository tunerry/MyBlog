import os
import requests
import threading
import queue
from io import BytesIO
from lxml import etree
from time import sleep
from selenium import webdriver
from django.core.files.base import ContentFile

class anime:
    def __init__(self, quarter, time, name, cover, introduction):
        self.quarter = quarter
        self.time = time
        self.name = name
        self.cover = cover
        self.introduction = introduction

class episode:
    def __init__(self, num, name, url, anime):
        self.num = num
        self.name = name
        self.url = url
        self.anime = anime


def decode(r):
    if r.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(r.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = r.apparent_encoding
        content = r.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return content

def dynamic(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    # 添加cookie
    browser.delete_all_cookies()
    # 携带cookie打开
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1565317100.805502,
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_auth",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "0475wSGBNO6gsF5K%2FVulvlzz8F1lZzx9HRPt1crfOOzmKXc%2B6vjEAMZzvJu4UlxlSQT5YDEdmLPOSABN6vL%2BwvanFjGv",
        "id": 1
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1533867646.383599,
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_lastact",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1533781250%09gact.php%09",
        "id": 2
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1536368322.5517,
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_lastvisit",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1533772726",
        "id": 3
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_lip",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "42.49.46.119%2C1533781224",
        "id": 4
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1536368322.55163,
        "hostOnly": True,
        "httpOnly": True,
        "name": "L8PX_2132_saltkey",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "j0G0BbCO",
        "id": 5
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1533867646.383458,
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_sid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "P6YTmC",
        "id": 6
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "hostOnly": True,
        "httpOnly": False,
        "name": "L8PX_2132_st_p",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "0%7C1533780852%7C0d5f3e216cd6552038bf209602b76740",
        "id": 7
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "hostOnly": True,
        "httpOnly": False,
        "name": "sohu_cy",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "038cj2b7lulsnkeeniggb9elu7",
        "id": 8
    })
    browser.add_cookie({
        "domain": "bbs.005.tv",
        "expirationDate": 1533782540.933747,
        "hostOnly": True,
        "httpOnly": False,
        "name": "sohu-cy",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "038cj2b7lulsnkeeniggb9elu7",
        "id": 9
    })
    browser.get(url)
    # 开爬
    s = browser.find_element_by_xpath('//div[@class="container clear"]/div[@class="clear"]/div[@class="player_main"]/iframe')
    return s.get_attribute('src')

def index(headers):
    r = requests.get('http://www.dilidili.wang/anime/201807/',headers=headers)
    content = decode(r)
    tree = etree.HTML(content)
    urls = tree.xpath('//div[@class="anime_list"]/dl/dd/h3/a/attribute::href')

    for i in range(0,len(urls)):
        """res = requests.get(pic)
        data = res.content"""
        urls[i] = 'http://www.dilidili.wang' + urls[i]

    return urls



def info(url, animes, episodes, headers):

    r = requests.get(url, headers=headers)
    content1 = decode(r)

    tree = etree.HTML(content1)
    name = tree.xpath('//div[@class="detail con24 clear"]/dl/dd/h1/text()')[0]
    quarter = tree.xpath('//div[@class="detail con24 clear"]/dl/dd/div[@class="d_label"][2]/a/text()')[0]
    introduction = tree.xpath('//div[@class="detail con24 clear"]/dl/dd/div[@class="d_label2"][3]/text()')[0]
    time = tree.xpath('//div[@class="detail con24 clear"]/dl/dd/div[@class="d_label2"][last()]/text()')[2]    #爬取到的列表中的第三个
    cover = tree.xpath('//div[@class="detail con24 clear"]/dl/dt/img/@src')[0]      #封面的url
    a = anime(quarter=quarter, time=time, name=name, cover=cover, introduction=introduction)
    animes.put(a)
    e_as = tree.xpath('//div[@class="time_pic list"]/div[1]/div/div/div/ul/li/a')      #第二层div有多个类似，需要从第一层找下来

    for e_a in e_as:
        e_url = e_a.xpath('string(@href)')
        e_r = requests.get(e_url,headers=headers)
        content2 = decode(e_r)
        e_tree = etree.HTML(content2)
        num = e_a.xpath('string(./em/span/text())')
        e_name = e_a.xpath('string(./em/text())')
        e_srcs = e_tree.xpath('//div[@class="container clear"]/div[@class="clear"]/div[@class="player_main"]/iframe/@src')
        e_src = ''
        if e_srcs != []:
            e_src = e_srcs[0]
        else:
            try:
                e_src = dynamic(e_url)
            except:
                print("Something wrong with dynamic!!")
                print("{} 第{}集没链接！".format(a.name, num))
        e = episode(num, e_name, e_src, a)
        episodes.put(e)

flag = 1
def UpdateDB(a,e):
    while True:
        if not a.empty():
            an = a.get()
            finds = models.Anime.objects.filter(name=an.name)
            if (len(finds)):
                find = models.Anime.objects.get(name=an.name)
                if an.quarter != find.quarter or an.time != find.time or an.introduction != find.introduction:
                    find.quarter = an.quarter
                    find.time = an.time
                    find.introduction = an.introduction
                    find.save()
                    print("动画：{}  ——更新完毕！".format(an.name))

            else:
                #获取图片
                i = requests.get(an.cover)
                form = an.cover.split('.')
                img_content = ContentFile(i.content)
                new = models.Anime.objects.create(quarter = an.quarter, time = an.time, name = an.name, introduction = an.introduction)
                cname = an.name.replace('/', '-')
                new.cover.save(cname + '.' + form[-1], img_content)
                print("动画：{}  ——新增完毕！".format(an.name))


        if not e.empty():
            ep = e.get()
            ep_a = ep.anime
            finds = models.Episode.objects.filter(name=ep.name)
            if (len(finds)):
                find = models.Episode.objects.get(name=ep.name)
                if ep.num != find.num or ep.url != find.url:
                    find.num = ep.num
                    find.url = ep.url
                    find.save()
                    print("剧集：{}  ——更新完毕！".format(ep.name))
            else:
                find_a = models.Anime.objects.filter(name=ep_a.name)
                models.Episode.objects.create(num=ep.num, url=ep.url, name=ep.name,
                                                  anime=find_a[0])
                print("剧集：{}  ——新增完毕！".format(ep.name))

        if flag==0 and a.empty() and e.empty():
            break

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyCharm.settings")
    import django
    django.setup()
    from mysite1 import models
    #程序主体
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    print('正在爬取...')
    animes = queue.Queue()
    episodes = queue.Queue()
    urls = index(headers)
    t = threading.Thread(target=UpdateDB, args=[animes, episodes])
    t.start()
    for u in urls:
        info(u, animes, episodes, headers)
    flag = 0