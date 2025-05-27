#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：bhf
@Date    ：2025/2/28 10:30
@Desc    ：
"""
import requests
from queue import Queue
import threading
import requests
import time, re
import io, os
import random


user_agent_list = [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

    # IPhone
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPod
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPAD
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # Android
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # QQ浏览器 Android版本
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # Android Opera Mobile
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # Android Pad Moto Xoom
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # BlackBerry
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # WebOS HP Touchpad
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # Nokia N97
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # Windows Phone Mango
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC浏览器
    # "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # UCOpenwave
    "Openwave/ UCWEB7.0.2.37/28/999",
    # UC Opera
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 从多个uas里随机选择一个ua,能够降低被墙的几率
header={
    'User-Agent':random.choice(user_agent_list)
    }

# ip代理池
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
}
failed_text = "Your Browser Isn't Supported By Google Patents"


file_last_run_start_patent = './error/last_run_start_patent_id.txt'
file_last_run_finish_patent = './error/last_run_finish_patent_id.txt'
html_result_path = './html'


## 避免被墙现在主要通过2个举措， 1是增加ip代理池，每爬一批数据换一个ip，另外是每次更换请求头来模拟；
class Crawl_Thread(threading.Thread):
    '''
    抓取线程类，需要继承线程类Thread
    '''
    def __init__(self, thread_id, queue, first_id, block_num):
        threading.Thread.__init__(self) # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue # 任务队列
        self.first_id=first_id
        self.block_num = block_num
        self.init_folder()

    def init_folder(self):
        if not os.path.exists(f'{html_result_path}/{self.block_num}/'):
            os.makedirs(f'{html_result_path}/{self.block_num}/')

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        '''
        #print('启动线程：',self.thread_id)
        # 每个线程会执行获取每个专利所在页面的源代码
        self.crawl_spider()
        #print('退出了该线程：',self.thread_id)

    def crawl_spider(self):
        error_times=0
        while True:
            if self.queue.empty(): #如果队列为空，表明该年份专利爬完了,则跳出
                break
            else:
                patent_id = self.queue.get()
                #print('当前工作的线程为：',self.thread_id," 正在采集：",patent_id)
                # finish=False
                # while finish==False:
                # 每个专利详情页的url
                #url = f'https://patents.google.com/patent/CN{self.first_id}{patent_id:08}' #切换CN/EU
                url = f'https://patents.google.com/patent/EP{patent_id:07}'
                try:
                    # 获得专利详情页的源代码text
                    # response = requests.get(url,headers=header,proxies=proxies)
                    count = 0
                    while True:
                        header = {
                            'User-Agent': random.choice(user_agent_list)
                        }
                        response = requests.get(url, headers=header)
                        response.encoding = response.apparent_encoding
                        if failed_text not in response.text:
                            break
                        count += 1
                        if count >= 5:
                            break
                    # text_queue.put(item) # 将采集的结果放入text_queue中
                    finish = True
                except Exception as e:
                    # 连接次数过多,被服务器拒绝连接,增加延迟再访问
                    #print('采集线程错误',e)
                    # 放回队列让之后线程爬取
                    # self.queue.put(patent_id)
                    time.sleep(20)
                    # time.sleep(1)
                    continue
                if response.status_code != 200:
                    error_times += 1
                    if error_times == 50:
                        # 将队列置为空
                        print("已达到该年份最大专利号")
                        self.queue = Queue()
                        print(patent_id)
                        with open(file_last_run_finish_patent, mode='w', encoding='utf-8') as f_out:
                            f_out.write(str(patent_id))
                        error_flag = True
                    else:
                        continue
                else:
                    # 如果未达到最大值,则得到了页面源代码,则保存下text,之后有需要可以使用
                    #with open(f'{html_result_path}/{self.block_num}/CN{self.first_id}{patent_id:08}.html', mode='w', encoding='utf-8') as f_out: #切换CN/EU
                    with open(f'{html_result_path}/{self.block_num}/EP{patent_id:07}.html', mode='w', encoding='utf-8') as f_out:
                        f_out.write(response.text)


def main():
    """
    申请号说明
    https://www.lexology.com/library/detail.aspx?g=bd71309d-1657-402e-a6cf-0e37ec2af28c
     """
    # CN100998275
    # first_id=[1]
    first_id = 1
    # 当连续2000个patent_id都爬取失败，则表明该年份没有专利，或者网络error，跳出循环
    global error_flag
    error_flag = False
    # 每次保证block_size大小的专利完整下载
    block_size = 100000
    max_patent_id = 19522657
    # 判断文件是否存在，如果不存在则创建
    if not os.path.exists(file_last_run_start_patent):
        block_num_start = 0
    else:
        with open(file_last_run_start_patent, mode='r', encoding='utf-8') as f_in:
            patent_id=f_in.read()
        block_num_start=max((max_patent_id - int(patent_id))//block_size, 0)

    # 按照年份爬取，从最新的2025年开始爬取
    for block_num in range(block_num_start, 7):
        start_time = time.time()

        # 如果年份的爬取完了，则终止
        if error_flag:
            break
        # 每个block起始id
        start_id = max_patent_id - block_size*(block_num)
        end_id = start_id - block_size
        print(f"Start download block：{block_num}，patent_id：{start_id}-{end_id}")

        with open(file_last_run_start_patent, mode='w',encoding='utf-8') as f_out:
            f_out.write(str(start_id))
        # 结束id=起始id+队列大小,即把所有id存入Queue中
        # crawl线程个数
        crawl_threads_num = 40
        # 任务队列，存放网页id的队列
        q_size = 1500000
        patent_id_Queue = Queue(q_size)
        start_id = min(start_id, max_patent_id)
        patent_ids = [i for i in range(end_id, start_id)]
        patent_ids.reverse()
        for patent_id_ in patent_ids:
            # 构造任务队列
            patent_id_Queue.put(patent_id_)
        # 初始化采集线程
        crawl_threads = []
        crawl_name_list = [f'crawler_{i}' for i in range(crawl_threads_num)] # 总共构造i个爬虫线程
        for thread_id in crawl_name_list:
            thread = Crawl_Thread(thread_id,patent_id_Queue,first_id,block_num) # 实例化爬虫线程
            thread.start() # 启动线程
            crawl_threads.append(thread)

        # 等待队列情况，先进行网页的抓取
        while not patent_id_Queue.empty(): # 判断是否为空
            pass # 不为空，则继续阻塞
        craw_time=time.time()

        # 等待所有线程结束
        for t in crawl_threads:
            t.join()

        # 通知线程退出
        global flag
        flag = True
        end_time=time.time()

        #print(f'退出主线程！    time:{end-start}')
        print(f"block:{block_num}\tpatent_id:{start_id}-{end_id} has finished")
        print(f"Cost time of the block:{end_time-start_time}\ttotal {block_size}'s patent\tavg time:{block_size/(end_time-start_time)} num/s")
        # 该block下载时间：211.908784866333,共1000个专利，平均耗时：4.719011534282433个/s

# text_queue = Queue() # 存放解析数据的queue
flag = False
error_flag=False


if __name__ == '__main__':
    # 必须科学上网
    main()
