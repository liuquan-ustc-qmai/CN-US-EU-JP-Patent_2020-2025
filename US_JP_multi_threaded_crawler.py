import requests
from queue import Queue
import threading
import requests
import time,re
import io,os
import random
from bs4 import BeautifulSoup
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
    # Taobao
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # Liebao
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
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
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC
    "UCWEB7.0.2.37/28/999",
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
# Change to your own IP address and port number
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
}
failed_text = "Your Browser Isn't Supported By Google Patents"

class Crawl_Thread(threading.Thread):
    '''
        Inherit from the Thread class.
    '''
    def __init__(self,thread_id,queue,first_id,block_num):
        threading.Thread.__init__(self) # Need to initialize the constructor of the parent class
        self.thread_id = thread_id  
        self.queue = queue # Task queue
        self.first_id=first_id
        self.block_num=block_num

    def run(self):
        '''
        The thread will call the corresponding run method during the invocation process
        '''
        #print('Start thread：',self.thread_id)
        # Each thread executes the source code to get the page where each patent is located
        self.crawl_spider()
        #print('Exited the thread：',self.thread_id)

    def crawl_spider(self):
        error_times=0
        while True:
            if self.queue.empty(): #If the queue is empty, indicating that the patent has climbed out for that year, it will be out
                break
            else:
                patent_id = self.queue.get()
                #print('The currently running thread：',self.thread_id," Collecting：",patent_id)
                # finish=False
                # while finish==False:
                # The URL of each patent detail page
                #url = f'https://patents.google.com/patent/US{self.first_id}{int(patent_id):07d}' #switch US/JP
                url = f'https://patents.google.com/patent/JP{self.first_id}{int(patent_id):06d}'
                #print(url)
                try:
                    # Obtain the source code text of the patent details page
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
                        finish=True
                except Exception as e:
                    # Too many connection attempts, the server refuses to connect. Increase the delay before trying again.
                    #print('thread error',e)
                    # Put back in the queue for the subsequent threads to crawl.
                    # self.queue.put(patent_id)
                    time.sleep(20)
                    print('delay')
                    # time.sleep(1)
                    continue
                if response.status_code!=200:
                    # If it is reported 404 for ten consecutive times, it means that the maximum number has been reached, and it will jump out of the loop and continue to crawl in other years
                    error_times+=1
                    if error_times==50:
                        self.queue=Queue()
                        with open(f'./error/last_run_finish_patent_id.txt',mode='w',encoding='utf-8') as f_out:
                            f_out.write(str(patent_id))
                        error_flag=True
                        print('year finished')
                    else:
                        continue
                else:
                    if not os.path.exists(f'./data/html/{self.block_num}/'):
                        os.makedirs(f'./data/html/{self.block_num}/')
                    # If the maximum value is not reached, the source code of the page is obtained, and the text is saved, and then it can be used if necessary
                    # Perform a preliminary filter on the image to reduce the size
                    #with open(f'./data/html/{self.block_num}/US{self.first_id}{int(patent_id):07d}.html',mode='w',encoding='utf-8') as f_out: #switch US/JP
                    with open(f'./data/html/{self.block_num}/JP{self.first_id}{int(patent_id):06d}.html',mode='w',encoding='utf-8') as f_out:
                        response.raise_for_status
                        soup = BeautifulSoup(response.text, 'html.parser')
                        target_li = soup.find_all('li',{'itemprop':'images'})
                        for li in target_li:
                            li.decompose()
                        f_out.write(str(soup))
                        #print(f'store {patent_id}')


class Download_Thread(threading.Thread):
    def __init__(self,thread_id,queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        #print('Start the thread：', self.thread_id)
        # Use flag, wait for all the crawl threads to finish before the download thread can end
        while not flag:
            try:
                item = self.queue.get(False) # If the get parameter is false, the queue is empty and an exception is thrown
                if not item:
                    pass
                self.download_files(item)
                self.queue.task_done()
            except Exception as e:
                pass
        #print('Exited the thread：', self.thread_id)

    def download_files(self,item):
        #print('The current working thread：',self.thread_id," Collecting：",item['patent_id'])
        pdf_download_url = re.findall('<meta name="citation_pdf_url" content="(.*?)">',item['text'])[0]
        # Download
        response=requests.get(url=pdf_download_url,headers=header,proxies=proxies)
        bytes_io = io.BytesIO(response.content)
        with open(f"./pdf/{item['patent_id']}.PDF", mode='wb') as f:
            f.write(bytes_io.getvalue())


def main():
    # US20250072306
    # first_id=[2020,2021,2022,2023,2024,2025]
    first_id=2025
    # When 2,000 consecutive patent_id fail to crawl, it means that there are no patents in that year, or the network error is out of the loop
    global error_flag
    error_flag=False
    # Guaranteed block_size-sized patent full download each time
    block_size=100000
    min_patent_id = 1
    # Determine whether a file exists, and if it does not, create it
    if not os.path.exists('./error/last_run_start_patent_id.txt'):
        block_num_start=0
    else:
        with open(f'./error/last_run_start_patent_id.txt',mode='r',encoding='utf-8') as f_in:
            patent_id=f_in.read()
        block_num_start=max((int(patent_id)-min_patent_id)//block_size,0)
    for block_num in range(block_num_start,3):
        if not os.path.exists(f'./Patent/html/{block_num}'):
            os.makedirs(f'./Patent/html/{block_num}')
        start_time=time.time()
        if error_flag:
            break
        # The starting ID of each block
        start_id=min_patent_id+block_size*(block_num)
        end_id=start_id+block_size
        print(f"Start download block：{block_num}，patent_id：{start_id}-{end_id}")

        with open(f'./error/last_run_start_patent_id.txt',mode='w',encoding='utf-8') as f_out:
            f_out.write(str(start_id))
        # End id = start id Queue size, all IDs are stored in the queue
        # The number of crawl threads
        crawl_threads_num=40
        download_thread_num=100
        # Task queue, a queue that stores web page IDs
        q_size=1000000
        patent_id_Queue = Queue(q_size)
        start_id = max(start_id,min_patent_id)
        
        for patent_id in range(start_id,end_id): 
            # Splice into patent_id
            patent_id=f'{patent_id}'
            # Construct a task queue
            patent_id_Queue.put(patent_id)
        # Initialize the acquisition thread
        crawl_threads = []
        #
        crawl_name_list = [f'crawler_{i}' for i in range(crawl_threads_num)] # A total of i crawler threads are constructed
        for thread_id in crawl_name_list:
            thread = Crawl_Thread(thread_id,patent_id_Queue,first_id,block_num) # Instantiate a crawler thread
            thread.start() # Start the thread
            crawl_threads.append(thread)

        # Wait for the queue situation and crawl the web page first
        while not patent_id_Queue.empty(): # Determine whether it is empty
            pass # If it is not empty, it will continue to block
        craw_time=time.time()
        #print(f'crawl thread finish!     time:{craw_time-start}')
        # Wait for all threads to end
        for t in crawl_threads:
            t.join()
        # while not text_queue.empty():
        #     pass
        # Notify the thread to exit
        global flag
        flag = True
        #print('download thread finish!')
        end_time=time.time()
        # for t in download_thread:
        #     t.join() # Wait for all threads to execute here before continuing to execute

        #print(f'Exit the main thread！    time:{end-start}')
        print(f"block:{block_num}\tpatent_id:{start_id}-{end_id} has finished")
        print(f"Cost time of the block:{end_time-start_time}\ttotal {block_size}'s patent\tavg time:{block_size/(end_time-start_time)} num/s")
flag = False
error_flag=False
if __name__ == '__main__':
    main()
