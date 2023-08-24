import urllib.request
from threading import Thread
from queue import Queue
from colorama import init
import ssl
import requests

init(autoreset=True)

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

def printf(text):
    ''.join([str(item) for item in text])
    print(text + '\n'),

def check_page_status(url):
    try:
        response = urllib.request.urlopen(url)
        status_code = response.getcode()
        return status_code
    except Exception as e:
        return 'Error'

def is_page_blank(url):
    try:
        status_code = check_page_status(url)
        if status_code != 200:
            return False
        
        context = ssl._create_unverified_context() 
        response = urllib.request.urlopen(url, context=context)
        content = response.read().decode('utf-8')

        if not content.strip():
            return True

        return False
    except Exception as e:
        print("Error:", e)
        return True

def main(url):
    try:
        text = '\033[32;1m#\033[0m ' + url
        if is_page_blank(url):
            text += ' => \033[32;1mBlank/Vuln\033[0m'
            with open('blank_pages.txt', 'a') as file:
                file.write(url + '\n')
        else:
            text += ' => \033[31;1mNormal\033[0m'
    except:
        text = '\033[31;1m#\033[0m ' + url
        text += ' => \033[31;1mError\033[0m'
    print(text)




if __name__ == '__main__':
    print("""

____    __    ____  _______ ____    __    ____ 
\   \  /  \  /   / |   ____|\   \  /  \  /   / 
 \   \/    \/   /  |  |__    \   \/    \/   /  
  \            /   |   __|    \            /   
   \    /\    /    |  |____    \    /\    /    
    \__/  \__/     |_______|    \__/  \__/     
                                               
    Just Blank Page Scanner - Recode Kece Finder \n""")
    try:
        filename = input("Enter the filename containing URLs (list.txt): ")
        num_threads = int(input("Enter the number of threads (1-999): "))
    except KeyboardInterrupt:
        print("Scan aborted by user.")
        exit()

    try:
        with open(filename, 'r') as file:
            urls = file.readlines()
    except:
        print("Error reading the file.")
        exit()

    pool = ThreadPool(num_threads)
    for url in urls:
        url = url.strip()
        if url:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url
            if url.endswith('/'):
                url = url[:-1]
            pool.add_task(main, url)
    
    pool.wait_completion()
