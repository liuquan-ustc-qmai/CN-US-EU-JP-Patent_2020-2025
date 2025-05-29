import json
from bs4 import BeautifulSoup
import re
import time
import os
import threading
import queue
import traceback

def extract_patent_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # 提取专利基本信息
    patent_info = {
        'publication_number': soup.find('dd', itemprop='publicationNumber').text if soup.find('dd', itemprop='publicationNumber') else None,
        'title': soup.find('span', itemprop='title').text.strip() if soup.find('span', itemprop='title') else None,
        'authority': [soup.find('dd', itemprop='countryCode').text.strip(), soup.find('dd', itemprop='countryName').text.strip()] if soup.find('dt', string='Authority') else None,
        'prior_art_keywords': [item.text.strip() for item in soup.find_all('dd', itemprop='priorArtKeywords')] if soup.find('dt', string='Prior art keywords') else None,
        'legal_status': soup.find('span', itemprop='status').text.strip() if soup.find('span', itemprop='status') else None,
        'application_number': soup.find('dd', itemprop='applicationNumber').text.strip() if soup.find('dd', itemprop='applicationNumber') else None,
        'inventors': [inventor.text for inventor in soup.find_all('dd', itemprop='inventor')] if soup.find('dd', itemprop='inventor') else None,
        'current_assignee': soup.find('dd', itemprop='assigneeCurrent').text.strip() if soup.find('dd', itemprop='assigneeCurrent') else None,
        'original_assignee': soup.find('dd', itemprop='assigneeOriginal').text.strip() if soup.find('dd', itemprop='assigneeOriginal') else None,
        'abstract': soup.find('section', itemprop='abstract').find('div').text.strip() if soup.find('section', itemprop='abstract') else None,
        'priority_date': soup.find('time', itemprop='priorityDate')['datetime'] if soup.find('time', itemprop='priorityDate') else None,
        'filing_date': soup.find('time', itemprop='filingDate')['datetime'] if soup.find('time', itemprop='filingDate') else None,
        'publication_date': soup.find('time', itemprop='publicationDate')['datetime'] if soup.find('time', itemprop='publicationDate') else None,
        'classifications': [{
            "code": item.find_all("span", itemprop="Code")[-1].text if item.find_all("span", itemprop="Code") else None,
            "description": item.find_all("span", itemprop="Description")[-1].text if item.find_all("span", itemprop="Description") else None} for item in soup.find_all("ul", itemprop="classifications")],
        'definitions': [{
            "subject": item.find("span", itemprop="subject").text if item.find("span", itemprop="subject") else None,
            "definition": item.find("span", itemprop="definition").text if item.find("span", itemprop="definition") else None,
            "num_attr": item.find("meta", itemprop="num_attr").get('content') if item.find("meta", itemprop="num_attr") else None} for item in soup.find_all("li", itemprop="definitions")],
        'landscapes': [{
            "name": item.find("span", itemprop="name").text if item.find("span", itemprop="name") else None,
            "type": item.find("span", itemprop="type").text if item.find("span", itemprop="type") else None} for item in soup.find_all("li", itemprop="landscapes")],
        'description': soup.find('section', itemprop='description').find("div").text.replace('\n\n','\n').strip() if soup.find('section', itemprop='description') else None,
        'claims': soup.find('section', itemprop='claims').find('div').text.replace('\n\n','\n').strip() if soup.find('section', itemprop='claims') else None,   
        'n_claims': int(soup.find('section', itemprop='claims').find('h2').text.split('(')[1].split(')')[0]) if soup.find('section', itemprop='claims') else 0,
        'family_id': soup.find('section', itemprop='family').find('h2').text.strip() if soup.find('section', itemprop='family') else None,
        'citations': [item.text.replace('  ','').replace('\n\n','\n').strip() for item in soup.find_all('tr', itemprop='backwardReferencesOrig')] if soup.find('tr', itemprop='backwardReferencesOrig') else None,
        'n_citations': int(soup.find('h2', string=re.compile(r'Citations \(\d+\)')).text.split('(')[1].split(')')[0]) if soup.find('h2', string=re.compile(r'Citations \(\d+\)')) else 0,
        'cited_by': [item.text.replace('  ','').replace('\n\n','\n').strip() for item in soup.find_all('tr', itemprop='forwardReferences')] if soup.find('tr', itemprop='forwardReferences') else None,
        'n_citedby': int(soup.find('h2', string=re.compile(r'Cited By \(\d+\)')).text.split('(')[1].split(')')[0]) if soup.find('h2', string=re.compile(r'Cited By \(\d+\)')) else 0,
        'families_citing_this_family': [item.text.replace('  ','').replace('\n\n','\n').strip() for item in soup.find_all('tr', itemprop='forwardReferencesFamily')] if soup.find('tr', itemprop='forwardReferencesFamily') else None,
        'n_fctf': int(soup.find('h2', string=re.compile(r'Families Citing this family \(\d+\)')).text.split('(')[1].split(')')[0]) if soup.find('h2', string=re.compile(r'Families Citing this family \(\d+\)')) else 0,
        'family_cites_families': [item.text.replace('  ','').replace('\n\n','\n').strip() for item in soup.find_all('tr', itemprop='backwardReferencesFamily')] if soup.find('tr', itemprop='backwardReferencesFamily') else None,
        'n_fcf': int(soup.find('h2', string=re.compile(r'Family Cites Families \(\d+\)')).text.split('(')[1].split(')')[0]) if soup.find('h2', string=re.compile(r'Family Cites Families \(\d+\)')) else 0
    }
    return patent_info
'''
备用字段
'similar_patents': [{
            'number': patent.find('span', itemprop='publicationNumber').text if patent.find('span', itemprop='publicationNumber') else None,
            'title': patent.find('td', itemprop='title').text.strip() if patent.find('td', itemprop='title') else None
        } for patent in soup.find_all('tr', itemprop='similarDocuments')],
'''
# 示例使用
def txt_one(patent_path, txt_folder):
    with open(patent_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    patent_data = extract_patent_info(html_content)

    with open(f"{txt_folder}/{patent_path.split('/')[-1].split('.')[0]}.txt", 'w',encoding='utf-8') as fw:
        fw.write(str(patent_data))


def txt_folder(folder_path, error_log_file, max_threads=40):
    begint=time.time()
    txt_folder = f"{folder_path}_txt"
    if not os.path.exists(txt_folder):
        os.mkdir(txt_folder)
    try:
        all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                    if os.path.isfile(os.path.join(folder_path, f))]
    except Exception as e:
        print(f"无法读取文件夹 {folder_path}: {str(e)}")
        return

    # 创建线程安全的队列和错误日志文件
    file_queue = queue.Queue()
    error_lock = threading.Lock()
    
    # 将文件放入队列
    for file_path in all_files:
        file_queue.put(file_path)

    # 工作线程函数
    def worker():
        while True:
            try:
                file_path = file_queue.get_nowait()
            except queue.Empty:
                break  # 队列为空，工作完成
                
            try:
                # 处理单个文件
                txt_one(file_path,txt_folder)
            except Exception as e:
                # 记录错误到日志文件
                with error_lock:
                    with open(error_log_file, 'a') as f:
                        f.write(f"{file_path}\n")
                        traceback.print_exc(file=f)  # 记录完整的错误信息
                print(f"处理文件 {file_path} 时出错: {str(e)}")
            finally:
                file_queue.task_done()

    # 创建并启动线程
    threads = []
    for i in range(max_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # 等待所有线程完成
    for t in threads:
        t.join()


    endt=time.time()
    print(f"处理完成。cost time:{endt-begint}。错误日志保存在 {error_log_file}")


if __name__ == '__main__':
    #file_path = 'CN118522650.html'
    #txt_one(file_path, '.')
    folder_path = './15' #此处修改文件夹名
    error_log_file = folder_path[-1] + '_error_log.txt'
    txt_folder(folder_path, error_log_file)
