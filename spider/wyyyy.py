import os
from selenium import webdriver


def index(headers):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://music.163.com/#/user/home?id=102746132')
    browser.switch_to.frame("g_iframe")
    s = browser.find_elements_by_xpath('//div[@class="g-bd"]/div[@class="g-wrap p-prf"]/ul[@id="cBox"]/li/div[@class="u-cover u-cover-1"]/a')
    #print(s.get_attribute('class'))
    list_dic = {}
    for list in s:
        url = list.get_attribute('href')
        name = list.get_attribute('title')
        list_dic[name] = url

    return list_dic

def dynamic(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    browser.switch_to.frame("g_iframe")
    s = browser.find_elements_by_xpath(
        '//div[@class="j-flag"]/table/tbody/tr/td/div/div/div/span/a/b')

    for i in s:
        print(i.get_attribute('title'))

if __name__ == '__main__':
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    print('正在爬取...')

    dic = index(headers)

    for key, value in dic.items():
        print('歌单：%s' % key)
        dynamic(value)