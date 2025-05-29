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
    # Chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # Taobao
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # Liebao
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC
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
    # QQ-Android
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
    # UC
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

# Randomly selecting a ua from multiple uas
header={
    'User-Agent':random.choice(user_agent_list)
    }

# IP proxy pool
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
}
failed_text = "Your Browser Isn't Supported By Google Patents"


file_last_run_start_patent = './error/last_run_start_patent_id.txt'
file_last_run_finish_patent = './error/last_run_finish_patent_id.txt'
html_result_path = './html'


## Change the IP for each batch of data crawled, and also change the request headers each time
class Crawl_Thread(threading.Thread):
    '''
    Inherit from the Thread class
    '''
    def __init__(self, thread_id, queue, first_id, block_num):
        threading.Thread.__init__(self) # Need to initialize the constructor of the parent class.
        self.thread_id = thread_id
        self.queue = queue # Task queue
        self.first_id=first_id
        self.block_num = block_num
        self.init_folder()

    def init_folder(self):
        if not os.path.exists(f'{html_result_path}/{self.block_num}/'):
            os.makedirs(f'{html_result_path}/{self.block_num}/')

    def run(self):
        '''
        The thread will call the corresponding run method during the invocation process
        '''
        #print('Start thread：',self.thread_id)
        # Each thread will execute to retrieve the source code of the page where each patent is located
        self.crawl_spider()
        #print('Exited the thread：',self.thread_id)

    def crawl_spider(self):
        error_times=0
        while True:
            if self.queue.empty(): #If the queue is empty, it indicates that the patent search for that year is complete, then exit
                break
            else:
                patent_id = self.queue.get()
                #print('The current working thread is:',self.thread_id," Collecting：",patent_id)
                # finish=False
                # while finish==False:
                # The URL of each patent detail page
                #url = f'https://patents.google.com/patent/CN{self.first_id}{patent_id:08}' #Switch CN/EU
                url = f'https://patents.google.com/patent/EP{patent_id:07}'
                try:
                    # Obtain the source code text of the patent detail page
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
                    # text_queue.put(item) # Place the collected results into the text_queue
                    finish = True
                except Exception as e:
                    # Too many connection attempts, the server refused the connection, increase the delay before accessing again
                    #print('Collection thread error',e)
                    # Put it back in the queue for the subsequent thread to crawl
                    # self.queue.put(patent_id)
                    time.sleep(20)
                    # time.sleep(1)
                    continue
                if response.status_code != 200:
                    error_times += 1
                    if error_times == 50:
                        # Set the queue to empty
                        print("The maximum patent number for that year has been reached")
                        self.queue = Queue()
                        print(patent_id)
                        with open(file_last_run_finish_patent, mode='w', encoding='utf-8') as f_out:
                            f_out.write(str(patent_id))
                        error_flag = True
                    else:
                        continue
                else:
                    # If obtained the page source code, then save the text, which can be used later if needed.
                    #with open(f'{html_result_path}/{self.block_num}/CN{self.first_id}{patent_id:08}.html', mode='w', encoding='utf-8') as f_out: #Switch CN/EU
                    with open(f'{html_result_path}/{self.block_num}/EP{patent_id:07}.html', mode='w', encoding='utf-8') as f_out:
                        f_out.write(response.text)


def main():
    # CN100998275
    # first_id=[1]
    first_id = 1
    # If there are continuous 2000 patent_ids that fail to be crawled, it indicates that there are no patents for that year, or there is a network error, breaking the loop
    global error_flag
    error_flag = False
    # Ensure the complete download of the patent with a block_size of each time
    block_size = 100000
    max_patent_id = 19522657
    # Determine if the file exists, and if not, create it
    if not os.path.exists(file_last_run_start_patent):
        block_num_start = 0
    else:
        with open(file_last_run_start_patent, mode='r', encoding='utf-8') as f_in:
            patent_id=f_in.read()
        block_num_start=max((max_patent_id - int(patent_id))//block_size, 0)

    # Crawl according to the serial number, starting from the newest
    for block_num in range(block_num_start, 7):
        start_time = time.time()

        # If the crawling is completed, then terminate
        if error_flag:
            break
        # Starting ID of each block
        start_id = max_patent_id - block_size*(block_num)
        end_id = start_id - block_size
        print(f"Start download block：{block_num}，patent_id：{start_id}-{end_id}")

        with open(file_last_run_start_patent, mode='w',encoding='utf-8') as f_out:
            f_out.write(str(start_id))
        # End id = start id + queue size, which means putting all ids into the Queue
        # Number of crawl threads
        crawl_threads_num = 40
        # Task queue, a queue that stores webpage IDs
        q_size = 1500000
        patent_id_Queue = Queue(q_size)
        start_id = min(start_id, max_patent_id)
        patent_ids = [i for i in range(end_id, start_id)]
        patent_ids.reverse()
        for patent_id_ in patent_ids:
            # Construct a task queue
            patent_id_Queue.put(patent_id_)
        # Initialize collection thread
        crawl_threads = []
        crawl_name_list = [f'crawler_{i}' for i in range(crawl_threads_num)] # A total of i crawler threads are constructed
        for thread_id in crawl_name_list:
            thread = Crawl_Thread(thread_id,patent_id_Queue,first_id,block_num) # Instantiate the crawler thread
            thread.start() # Start thread
            crawl_threads.append(thread)

        # Waiting for the queue situation, first proceed with web scraping
        while not patent_id_Queue.empty(): # Determine if it is empty
            pass # If not empty, continue to block
        craw_time=time.time()

        # Wait for all threads to finish
        for t in crawl_threads:
            t.join()

        # Notify thread to exit
        global flag
        flag = True
        end_time=time.time()

        #print(f'Exit the main thread！    time:{end-start}')
        print(f"block:{block_num}\tpatent_id:{start_id}-{end_id} has finished")
        print(f"Cost time of the block:{end_time-start_time}\ttotal {block_size}'s patent\tavg time:{block_size/(end_time-start_time)} num/s")
        
# text_queue = Queue() # Queue for storing parsed data
flag = False
error_flag=False


if __name__ == '__main__':
    main()
