import random
import time

import requests
from lxml import etree
from urllib3.exceptions import ConnectTimeoutError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

cookie = "channelid=0; sid=1632914464897787; _gcl_au=1.1.1329272827.1632914468; _ga=GA1.2.136246139.1632914468; _gid=GA1.2.2040901549.1632914468; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1632914468; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1632917719"
headers = {
    'cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
def get_proxy(n):
    proxyList=[]
    content1=session.get("https://www.kuaidaili.com/free/inha/{}/".format(n)).content
    content=etree.HTML(content1.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))
    ip=content.xpath(' //td[@data-title="IP"]/text()')
    port=content.xpath(' //td[@data-title="PORT"]/text()')
    for i in range(1,len(ip)):
        temp=str(ip[i])+":"+port[i]
        proxyList.append(temp)
    return proxyList
def ip_main(n):
    for i in range(n):
        yield get_proxy(n)
        time.sleep(2)

def save_ip(ip):
    with open("ip.txt", "w+", encoding="utf-8") as f:
        f.write("\n".join(ip))
    f.close()
def get_random_ip():
    result=[]
    with open("ip.txt", "r", encoding="utf-8") as f:
        res=f.readlines()
        for i in res:
            result.append(i.strip("\n"))
    f.close()
    le=len(result)
    return str(result[random.randint(0,le)])
if __name__ == '__main__':
    for i in ip_main(3):
        save_ip(i)