# -*- coding: UTF-8 -*-
import csv
import time
import requests
from lxml import etree
import re
import os
import shutil
import concurrent.futures
import settings
s=settings.settings()

class noveldl():
    def __init__(self):
        # 小说主地址，后接小说编号,but好像没什么用
        self.req_url_base = s.req_url_base
        # 头文件，可用来登陆，cookie可在浏览器或者client.py中获取
        self.headerss = s.headers
        self.percent = 0
        self.index = []  # 目录
        self.titleindex = []  # 标题
        self.Summary = []  # 内容提要
        self.fillNum = ''  # 章节填充位数
        self.rollSign = []  # 卷标
        self.rollSignPlace = []  # 卷标位置
        self.href_list = []  # 章节链接
        self.td = []
        self.path = ''
        self.titleInfo = [1, 1, 1]
        self.fontlist = []

    def clear(self):
        self.percent = 0
        self.index = []
        self.titleindex = []
        self.Summary = []
        self.fillNum = 0
        self.rollSign = []
        self.rollSignPlace = []
        self.href_list = []
        self.td = []
        self.path = ''
        self.fontlist = []

    # 下载单章
    def get_sin(self, l,FILE_PATH):
        self.result=""
        titleOrigin = l.split('=')
        i = self.href_list.index(l)
        dot = ''
        badgateway = True
        while (badgateway):
            cont = requests.get(l, headers=self.headerss)
            dot = etree.HTML(cont.content.decode('gb18030', "ignore").encode("utf-8").decode('utf-8'))
            codetext = etree.tostring(dot, encoding="utf-8").decode()
            bdw = re.findall('<h1>502 Bad Gateway</h1>', codetext)
            if bdw == []:
                badgateway = False
            else:
                time.sleep(1)

            # tex:正文
        tex = dot.xpath('//*[@id="oneboolt"]//tr[2]/td[1]/div/text()')

        # tex1:作者有话要说
        tex1 = dot.xpath("//div[@class='readsmall']/text()")
        # sign:作者有话要说位置
        sign = dot.xpath("//*[@id='oneboolt']//tr[2]/td[1]/div/div[4]/@class")

        title = ''
        # 序号填充
        if self.titleInfo[0] == '1':
            title = str(titleOrigin[2]).zfill(self.fillNum) + "#"
        # 章节名称
        if self.titleInfo[1] == '1':
            title = title + " " + self.titleindex[i].strip()
        # 内容提要
        if self.titleInfo[2] == '1':
            title = title + " " + self.Summary[i].strip()

        title = re.sub('&amp;', '&', title)
        title = re.sub('&lt;', '<', title)
        title = re.sub('&gt;', '>', title)

        if self.href_list[i] in self.rollSignPlace:
            v = self.rollSign[self.rollSignPlace.index(l)]

        # 创建章节文件
        fo = open(FILE_PATH+"\\z" + str(titleOrigin[2].zfill(4)) + ".train_txt", 'w', encoding='utf-8')
        # 写入卷标
        if self.href_list[i] in self.rollSignPlace:
            v = re.sub('&amp;', '&', v)
            v = re.sub('&lt;', '<', v)
            v = re.sub('&gt;', '>', v)
            self.result+=v.strip()
            print("\r\n" + v + "\r\n")
            self.result+=title
        # 写入标题
        else:
            self.result += title
            fo.write("\r\n\r\n" + title + "\r\n")
        if len(tex) == 0 :
            self.result+="下载失败"
            fo.write('下载失败！')
        else:
            # 作话在文前的情况
            if str(sign) == "['readsmall']":
                for m in tex1:  # 删除无用文字及多余空格空行
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&amp;', '&', v)
                    v = re.sub('&lt;', '<', v)
                    v = re.sub('&gt;', '>', v)
                    v = re.sub('作者有话要说：', '作者有话要说：\n', v)
                    if v != "":  # 按行写入正文
                        self.result+=v+"\n"
                        fo.write(v + "\n")
                if len(tex1) != 0:
                    self.result+="\n*\r\n"
                    fo.write("\n*\r\n")
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&amp;', '&', v)
                    v = re.sub('&lt;', '<', v)
                    v = re.sub('&gt;', '>', v)
                    if v != "":
                        self.result+="\n"
                        fo.write(v + "\n")
            else:  # 作话在文后的情况
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&amp;', '&', v)
                    v = re.sub('&lt;', '<', v)
                    v = re.sub('&gt;', '>', v)
                    if v != "":
                        self.result+=v
                        fo.write(v + "\n")
                if len(tex1) != 0:
                    self.result+="\n*\r\n"
                    fo.write("\n*\r\n")
                for m in tex1:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&amp;', '&', v)
                    v = re.sub('&lt;', '<', v)
                    v = re.sub('&gt;', '>', v)
                    v = re.sub('作者有话要说：', '作者有话要说：\n', v)
                    if v != "":
                        self.result+=v+"\n"
                        fo.write(v + "\n")
        fo.close()
        self.percent += 1

    def get_txt(self, txt_id, threadnum, BASEE_FILE_PATH):
        # f=open("简介.csv","a",encoding="utf-8",newline="")
        TOC_csv_temp=[]

        # s.TOC_csv_f.writerow(s.TOC_csv_information)
            # f.close()
        self.percent = 0
        self.index = []
        self.titleindex = []
        self.Summary = []
        self.fillNum = 0
        self.rollSign = []
        self.rollSignPlace = []
        self.href_list = []
        self.td = []
        # 获取文章网址
        req_url = str(txt_id)
        # 通过cookie获取文章信息

        res = requests.get(req_url, headers=self.headerss).content
        # 对文章进行编码
        ress = etree.HTML(res.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))
        # 获取文案
        intro = ress.xpath("//html/body/table//tr/td[1]/div[2]/div[@id='novelintro']//text()")
        # 获取标签
        info = ress.xpath("string(/html/body/table[1]//tr/td[1]/div[3])")
        infox = []
        for i in range(1, 7):
            infox.append(ress.xpath("string(/html/body/table[1]//tr/td[3]/div[2]/ul/li[" + str(i) + "])"))
        # 获取标题和作者
        xtitle = ress.xpath('string(//*[@itemprop="articleSection"])').strip()
        TOC_csv_temp.append(str(xtitle).strip())
        xaut = ress.xpath('string(//*[@itemprop="author"])').strip()
        # 也可以做文件夹名字
        ti = xtitle + '-' + xaut
        print("网址：" + req_url + "\r\n小说信息：" + str(ti) + "\r\n")
        file1=os.listdir(s.BASEE_FILE_PATH+"\\result_txt")
        for file2 in file1:
            if ti in file2:
                print("网址：" + req_url + "\r\n小说信息：" + str(ti) + "已下载\r\n")
                time.sleep(1)
                return
        # 获取所有章节网址、标题、内容提要
        self.td = ress.xpath('//*[@id="oneboolt"]//tr')
        loc = []
        self.jt=[]
        self.all_page=0
        self.can_page=0
        # self.jt=[]
        for i in self.td:
            # href
            u = i.xpath('./td[2]/span/div[1]/a/@href')
            x = i.xpath('./td[2]/span/div[1]/a[1]/@rel')
            if len(u) > 0:

                self.all_page = self.all_page + 1
                self.can_page = self.can_page + 1
                self.href_list += u
                # 标题
                v = i.xpath('./td[2]/span/div[1]/a')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                v = re.sub('</?\w+[^>]*>', '', v)
                self.titleindex.append(v.strip())
                v = i.xpath('./td[3]')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                v = re.sub('</?\w+[^>]*>', '', v)
                v = re.sub('&#13;', '', v)
                # 内容提要
                self.Summary.append(v.strip())
            elif len(x) > 0:
                self.all_page=self.all_page+1
                self.jt.append(self.all_page)
            elif i.xpath('./td[2]/span/div[1]/span') != []:
                loc.append(i.xpath('./td[1]/text()')[0].strip())

        # 获取卷标--》第几卷
        self.rollSign = ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']")
        # 获取卷标位置
        self.rollSignPlace = ress.xpath(
            "//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        self.rollSignPlace += ress.xpath(
            "//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

        # #修改卷标格式
        for rs in range(len(self.rollSign)):
            self.rollSign[rs] = etree.tostring(self.rollSign[rs], encoding="utf-8").decode().strip()
            self.rollSign[rs] = re.sub('</?\w+[^>]*>', '', self.rollSign[rs])
            self.rollSign[rs] = "§ " + self.rollSign[rs] + " §"
        print("可下载章节数：" + str(self.can_page) + "\r\n")
        if loc != []:
            i = ""
            for x in loc:
                i = i + x + " "
            print("被锁章节：" + i + "\r\n")
        # fillNum：填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
        self.fillNum = len(str(len(self.td) - 4))

        # 对标题进行操作，删除违规字符等
        ti = re.sub('[\/:*?"<>|]', '_', ti)
        # 若文件名不想加编号，可以将这行删除
        ti = ti + '.' + req_url.split('=')[1]
        ti = re.sub('\r', '', ti)

        # 打开小说文件写入小说相关信息
        # **********************************************************8
        path = s.BASEE_FILE_PATH
        FILE_PATH=s.BASEE_FILE_PATH
        self.path = path
        if os.path.exists(ti + '_txt'):
            FILE_PATH+= "\\" + ti + "_txt"
            # os.chdir(ti + '_txt')
        else:
            FILE_PATH += "\\" + ti + "_txt"
            os.mkdir(ti + '_txt')
            # os.chdir(ti + '_txt')
        # *******************************************************888
        ppp = FILE_PATH
        self.index = []
        # 写入文章信息页
        TOC = xtitle + '\n'
        TOC_csv_temp.append(str(xaut).strip())
        TOC_csv_temp.append(str(req_url).strip())
        TOC += '作者：' + xaut + "\r\n"
        TOC += '源网址：' + req_url + '\r\n'
        # 生成目录文字
        for l in self.href_list:
            titleOrigin = l.split('=')
            i = self.href_list.index(l)
            title = str(titleOrigin[2]).zfill(self.fillNum) + " "
            title = title + self.titleindex[i].strip() + " "
            title = title + self.Summary[i].strip()
            if self.href_list[i] in self.rollSignPlace:
                try:
                    v = self.rollSign[self.rollSignPlace.index(l)]
                    self.index.append(v)
                except IndexError:
                    pass
            self.index.append(title)
        for ix in infox:
            ix = ix.strip()
            ix = re.sub('\r\n', '', ix)
            # ix = re.sub(' +', '', ix)
            # print(ix)
            TOC_csv_temp.append(str(ix.split("：")[1]).strip())
            TOC += ix + "\r\n"
        TOC += "文案：\r\n"
        temp=[]
        for nx in intro:
            v = re.sub(' +', ' ', str(nx)).strip()
            if v != "":
                temp.append(v)
                TOC += v + "\n"
        TOC_csv_temp.append(str(temp).strip())
        info = re.sub(' +', ' ', info).strip()
        info = re.sub('搜索关键字', '\r\n搜索关键字', info)
        info = re.sub(' 一句话简介：', '一句话简介：', info)
        info = re.sub('\r\n \r\n 立意：', '\r\n立意：', info)
        temp=info
        try:
            temp=temp.split("内容标签：")[1].strip()
        except IndexError:
            pass
        temp=temp.split("搜索关键字：")
        # 内容标签
        try:
            TOC_csv_temp.append(str(temp[0].strip()).strip())
            temp=temp[1].strip()
            temp=temp.split("一句话简介：")
            TOC_csv_temp.append(str(temp[0].strip()).strip())
            temp=temp[1].strip()
            temp = temp.split("立意：")
            TOC_csv_temp.append(str(temp[0].strip()).strip())
        except IndexError:
            pass
        # TOC_csv_temp.append(temp[0].strip())


        TOC += info + "\n"
        fo = open(FILE_PATH + "\\TOC.train_txt", 'w', encoding='utf-8')
        txt_f=open("train_txt\\"+ti+".train_txt","w",encoding="utf-8")
        txt_f.write(",".join("%s" %a for a in TOC_csv_temp))
        # " ".join('%s' %a for a in lists)
        txt_f.close()
        fo.write(TOC)
        fo.close()
        s.TOC_csv_f.writerow(TOC_csv_temp)
        # f.close()
        TOC_csv_temp.clear()

        with concurrent.futures.ThreadPoolExecutor(max_workers=threadnum) as executor:
            tlist = {executor.submit(self.get_sin, i,FILE_PATH): i for i in self.href_list}
            for future in concurrent.futures.as_completed(tlist):
                if self.percent < self.all_page:
                    print('\r 下载进度：%d/%d/%d' % (self.percent, self.can_page,self.all_page), end='', flush=True)
            print('\r 下载完成，总进度：%d/%d/%d\r\n' % (self.percent,self.can_page,self.all_page), end='', flush=True)
        if self.jt!=[]:
            self.jt.sort()
            vs = ""
            for ss in self.jt:
                vs = vs + str(ss) + "|"
            print("\r\n未购买或加载失败章节：")
            print(str(vs[:-1] )+ "\r\n")
        # 整合
        f = open(BASEE_FILE_PATH+"\\result_txt\\"+ti + ".train_txt", 'w', encoding='utf-8')
        filenames = os.listdir(ppp)
        i = 0
        for filename in filenames:
            filepath = ppp + '\\' + filename
            for line in open(filepath, encoding='utf-8', errors='ignore'):
                f.writelines(line)
        f.close()

        # 这个函数多线程有问题
        # !!!!!!!!!!!!!!!!!!!!!!!!!!此处递归删除该文件夹下无用东西
        shutil.rmtree(FILE_PATH)

        print("\r\ntxt文件整合完成")
