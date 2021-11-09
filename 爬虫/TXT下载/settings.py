import csv
import os

class settings():
    def __init__(self):
        #输入cookie，例如：cookie='12qhfu3eibzcd...'
        self.cookie='uuid_tt_dd=10_35466271290-1631518333193-133328; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_35466271290-1631518333193-133328; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; __gads=ID=3ddb270142c3dc7a-22794fb29ccb00ee:T=1631528443:RT=1631528443:S=ALNI_MZro3LTbRscDEjrubt-vbx2R9STSg; c_dl_prid=-; c_dl_rid=1631528485532_571612; c_dl_fref=blog.csdn.net; c_dl_fpage=/download/m0_52957036/20590130; ssxmod_itna2=eqRx9D0Q0QGQD=A50Ly7tQLxBKDtezGqzW=D61U06D0y4rq03=dRLdvDwhn4jKD2iYD=; unlogin_scroll_step=1631874892761; ssxmod_itna=eqGhGKY50KiKBK0Q=GHvx1j+qDtXwUmoG8YuRDBkBeiNDnD8x7YDvA+qoA8Y8YoloP0YOYPOrftdtmS4xvibx15KDHxY=DU=oTPDxaq0rD74irDDxD3DbbdDSDWKD9D048yRvLKGWDbx=Df4DmDGYneqDgDYQDGMPjD7QDIq6=YD64232B+l6Y3CGxiqDMIeGXYgWQkeaaoBU4xan7+GDDCxy40=htYGeVbrQDzk7DtkUB0TLYX16lAuNz8fhqA7vKSG+YboMYSD4riR4rV6qb87h5jYMK+GmNSAYQfS8xD=; c_hasSub=true; csdn_highschool_close=nologin_close; dc_session_id=10_1631885522704.797428; referrer_search=1631887564567; dc_sid=f94c5b0cc31441b8d3f1f11fac8b019f; c_first_ref=cn.bing.com; c_segment=0; c_first_page=https%3A//blog.csdn.net/qq_43710705/article/details/104234430; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1631886759,1631887530,1631888441,1631888648; c_pref=https%3A//cn.bing.com/; c_ref=https%3A//blog.csdn.net/qq_43710705/article/details/104234430; log_Id_click=33; c_utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.no_search_link; c_page_id=default; dc_tos=qzl2fw; log_Id_pv=41; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1631890077; log_Id_view=136'
        #线程池最大容量（数字越大，占据内存等资源越多，数字越小，下载越慢，总之看个人电脑状况决定）
        self.ThreadPoolMaxNum=100
        self.headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.base_book_url = 'http://www.jjwxc.net/'
        self.csv_information = ["作者", "作品", "类型", "风格", "进度", "字数", "作品积分", "发表时间", "作品url"]
        self.BASEE_FILE_PATH = os.getcwd()
        self.csv_path=self.BASEE_FILE_PATH+"\\csv\\information.csv"

        self.base_url="http://www.jjwxc.net/bookbase_slave.php?page="
        self.csv_url_path=self.BASEE_FILE_PATH+"\\csv\\url.train_txt"
        self.has_downloaded_path=self.BASEE_FILE_PATH+"\\csv\\has_download.train_txt"
        self.req_url_base = 'http://www.jjwxc.net/onebook.php?novelid='
        self.TOC_csv_information=["作品名称","作者","源网址","文章类型",
                                 "作品视角","作品风格","所属系列",
                                 "文章进度","全文字数","文案",
                                 "内容标签","搜索关键字","一句话简介","立意"]
#            作品名称
#         self.TOC_csv_temp=[]
        self.TOC_csv_f=csv.writer(open("简介.csv","a+",encoding="utf-8",newline=""))
        self.writer=csv.writer(open(self.csv_path,"a",encoding="utf-8",newline=""))
        # with open(s.csv_path, "a", encoding="utf-8", newline="") as f:
        #     writer = csv.writer(f)
        # self.txt_path=open("train_txt\\")