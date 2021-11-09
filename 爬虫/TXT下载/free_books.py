# -*- coding: UTF-8 -*-

from main_txt import noveldl
import requests
from lxml import etree
import os
import settings
from get_ip import get_random_ip
s=settings.settings()
headers = s.headers
url_list=[]
completed=0
all=0
completed_page=0
base_book_url=s.base_book_url

def get_all_information(i_url):
    proxy = get_random_ip()
    res = requests.get(i_url, headers=headers,proxies=proxy).content
    # #对文章进行编码
    ress = etree.HTML(res.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))

    writer=s.writer
    # writer.writerow(information)
    base="//table[@class=\"cytable\"]//tr"
    for i in range(2,100):
        base_=base+"["+str(i)+"]"
        information_list = ress.xpath("string(" + base_ + ")")
        temp=[]

        if information_list=="":
            break
        for j in range(1,9):
            base__=base_+"/td"+"["+str(j)+"]"
            information= ress.xpath("string(" + base__ + ")").strip()

            temp.append(information)
        url_= base_book_url + ress.xpath(base_ + "/td[2]/a/@href")[0]
        temp.append(url_.strip())

        url_list.append(url_)
        writer.writerow(temp)
        # f.close()
        global all
        all=all+1
        temp.clear()
    # f.close()
    global completed_page
    completed_page=completed_page+1
    print("第%d页url爬取完成\n"%completed_page)

def get_book(i):
    c = noveldl()
    print("*********"+i+"***********")
    c.headerss = s.headers
    BASEE_FILE_PATH= s.BASEE_FILE_PATH
    c.get_txt(i, 100,BASEE_FILE_PATH)
    c.clear()
    pass
# def get_has_download_url():
#     downloaned_url=[]
#     try:
#         with open(s.has_downloaded_path,"r",encoding="utf-8") as f:
#             p=f.readlines()
#             for line in p:
#                 downloaned_url.append(line.strip("\n"))
#             f.close()
#     except AttributeError:
#         pass
#     return downloaned_url
# def append_downloaded_url(i):
#     with open(s.has_downloaded_path,"a+",encoding="utf-8") as f:
#         f.write(i+"\n")
#         f.close()
# def is_continued():
#     try:
#         first=os.stat(s.csv_url_path)
#         second=os.stat(s.has_downloaded_path)
#         if first.st_size==second.st_size-2:
#             return False
#     except AttributeError:
#         return True
#     return True
# def update_url():
#     global s
#     base_url = s.base_url
#     # #通过cookie获取文章信息
#     res = requests.get(base_url, headers=headers).content
#     # #对文章进行编码
#     ress = etree.HTML(res.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))
#     # 获取总页数
#     page_num = int(ress.xpath("string(//html/body/div[@class='controlbar']/font[1])").strip())
#     for i in range(1, page_num + 1):
#         url = base_url + str(i)
#         get_all_information(url, ress)
#     with open(s.csv_url_path, "w", encoding="utf-8") as f:
#         s = "\n".join(url_list)
#         f.write(s)
#         f.close()
#     print("更新完成.........")
# def quoted_url(downloaded_url):#去重
#     return list(set(url_list).difference(set(downloaded_url)))
def download_txt():
    # 控制下载的url个数,
    # if not is_continued():
    #     print("已下载完成")
    #     print("是否更新(y/n)")
    #     if input().lower()=="y":
    #         update_url()
    # downloaded_url=get_has_download_url()
    # url_list=quoted_url(downloaded_url)
    for i in url_list:
        get_book(i)
        print("下载完成")


def ttt_bo(s=None):
    base_url=s.base_url
    # #通过cookie获取文章信息
    res=requests.get(base_url,headers=headers).content
    # #对文章进行编码
    ress=etree.HTML(res.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
    # 获取总页数
    page_num=int(ress.xpath("string(//html/body/div[@class='controlbar']/font[1])").strip())

    # with concurrent.futures.ThreadPoolExecutor(max_workers=page_num) as executor:
    #     tlist={executor.submit(get_all_information,base_url+str(i),ress) :i for i in range(1,page_num+1)}
    #     for future in concurrent.futures.as_completed(tlist):
    #         if completed_page<page_num:
    #             print('\r 下载进度：%d/%d' % (completed_page,page_num), end='', flush=True)
    #         print('\r 下载进度：%d/%d\r\n' % (completed_page,page_num), end='', flush=True)
    #
    if not os.path.exists(s.csv_url_path):
        information = s.csv_information
        writer = s.writer
        writer.writerow(information)
        for i in range(1,page_num+1):
            url=base_url+str(i)
            get_all_information(url)
        with open(s.csv_url_path,"w",encoding="utf-8") as f:
            s="\n".join(url_list)
            f.write(s)
            f.close()
    else:
        with open(s.csv_url_path,"r",encoding="utf-8") as f:
            url_list1=f.readlines()
            for url in url_list1:
                url=str(url).strip()
                url_list.append(url)
            f.close()
    try:
        if not os.path.exists("简介.csv"):
            with open("简介.csv","w",encoding="utf-8",newline="") as f:
                f.write(",".join(s.TOC_csv_information))
        TOC_csv_f = s.TOC_csv_f
    except AttributeError:
        pass
    download_txt()
#     根据url获取数据
if __name__ == '__main__':
    try:
        ttt_bo(s)
    except FileNotFoundError:
        ttt_bo(s)
    # ttt_bo()





