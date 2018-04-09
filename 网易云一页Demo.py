# -*- coding: utf-8 -*-
import requests,json,os
import base64
import codecs
from Crypto.Cipher import AES
import pymysql

from bs4 import BeautifulSoup
import requests
import random


class Spider():
    def __init__(self):
        self.fromdata = {'params':'pGoByTtoHgPRVtO5tZmyIuVry/8KfR4Vi4In3w1GUxofi2YC964YIaHGBfbo46fbIv5iLB/KlxLxWys3CFegWuoFrAW85k4DScT55eqSDwWjFCltsJ+PNR2uEXMtPejNzksypB4gIlLhH2ejal601SsUXWB/EMPwOhmSJup1Yl1SvzYy8xC/TPIko4FLKig3',
                         'encSecKey':'bcfd7901b829840e2f98747e8705e780d694d61eca25103ab15826b6be88515e0b5495feb0a6edee840b04b64fb037fe700cbc59d7432848766339bc6e26f5ed38ef14cff9ca2ea227a7f1f843fd4a55c6f2bd0f9608002e3b40264b89a0bcdeaab331523350c0434a1b8e83d79d715021f7d367b175dc98da61ea2dc833c950'}
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016?csrf_token="
        #self.url = "http://www.xiami.com/commentlist/turnpage/id/1776156051/page/2/ajax/1"
    def __get_jsons(self,url):
        jsons = requests.post(url, data=self.fromdata, headers=self.header)
#        print(jsons.status_code)
#        print(jsons.text)
#        print(json.loads(jsons.text))
        num = 1
        for user in json.loads(jsons.text)['comments']:
#            print(num,end='')
            print(user['user']['nickname']+' : '+user['content']+' 点赞数：'+str(user['likedCount']))
            num += 1
    
    def run(self):
        self.__get_jsons(self.url)


#############z代理ip###################

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
#    print(proxies)

#############z代理ip###################





        
def main():
    spider = Spider()
    spider.run()
main()