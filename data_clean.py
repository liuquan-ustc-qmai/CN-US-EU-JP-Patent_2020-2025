import os
import ast
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

# 全局锁，用于安全写入结果文件夹
write_lock = threading.Lock()

def process_file(file_path, result_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            data = ast.literal_eval(content)
        #更改清洗阈值
        if data.get('publication_number') is None or data.get('classifications') is None or data.get('n_claims')<=5 \
		or max(data.get('n_citations'),data.get('n_citedby'),data.get('n_fctf'),data.get('n_fcf'))<=2: 
            pass
        else:
            with write_lock:
                shutil.copy2(file_path, result_dir)
    except:
        pass

def process_files_in_threads(directory, result_dir, max_workers=100):
    # 确保结果文件存在且为空
    os.makedirs(result_dir, exist_ok=True)
    
    # 获取所有txt文件
    start = 111522658 #此处更改编号起止，便于检测是否有缺漏
    end = start +500000
    file_paths = []
    for file in range(start, end):
        file = 'CN' + str(file) + '.txt' #根据国家更改首字母
        file_paths.append(os.path.join(directory, file))
    
    # 使用线程池处理文件
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_path in file_paths:
            executor.submit(process_file, file_path, result_dir)

if __name__ == "__main__":
    directory = './15_txt'  # 替换为待清洗文件夹路径
    result_dir = f'./cn_use' #设置输出文件夹
    begint = time.time()
    process_files_in_threads(directory, result_dir, max_workers=40)  # 可根据CPU核心数调整线程数
    endt = time.time()
    file_count = len(os.listdir(result_dir))
    print(f'文件夹{result_dir}中共有{file_count}个文件,耗时{endt-begint}秒')
