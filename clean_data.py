import os
import ast
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

# Global lock, used for securely writing to the results folder
write_lock = threading.Lock()

def process_file(file_path, result_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            data = ast.literal_eval(content)
        # Set the cleaning threshold
        if data.get('publication_number') is None or data.get('classifications') is None or data.get('n_claims')<=5 \
		or max(data.get('n_citations'),data.get('n_citedby'),data.get('n_fctf'),data.get('n_fcf'))<=2: 
            pass
        else:
            with write_lock:
                shutil.copy2(file_path, result_dir)
    except:
        pass

def process_files_in_threads(directory, result_dir, max_workers=100):
    # Make sure that the result file exists and is empty
    os.makedirs(result_dir, exist_ok=True)
    
    # Get all txt files
    start = 111522658 # The start and end of the number are changed here to make it easier to detect if there are any gaps
    end = start +500000
    file_paths = []
    for file in range(start, end):
        file = 'CN' + str(file) + '.txt' #Change the initials according to the country
        file_paths.append(os.path.join(directory, file))
    
    # Use the thread pool to process files
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_path in file_paths:
            executor.submit(process_file, file_path, result_dir)

if __name__ == "__main__":
    directory = './15_txt'  # Replace with the path of the folder to be cleaned
    result_dir = f'./cn_use' # Set the output folder
    begint = time.time()
    process_files_in_threads(directory, result_dir, max_workers=40)  # The number of threads can be adjusted according to the number of CPU cores
    endt = time.time()
    file_count = len(os.listdir(result_dir))
    print(f'There are {file_count} files in folder {result_dir}, taking {endt-begint} seconds.')
