from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from threading import Thread
from Queue import Queue
from colorama import init

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

def is_page_blank(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        chromedriver_path = '/usr/bin/chromedriver'  # Ganti dengan path yang sesuai
        driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)

        driver.get(url)

        # Menambahkan timeout untuk menunggu hingga halaman terbuka
        driver.implicitly_wait(15)  # Tunggu hingga 15 detik

        # Cek apakah body halaman kosong
        body = driver.find_element_by_tag_name('body')
        if not body.text.strip():
            return True
        return False
    except (WebDriverException, NoSuchElementException, TimeoutException) as e:
        print("Error:", e)
        return False
    finally:
        driver.quit()

def main(url):
    try:
        text = '\033[32;1m#\033[0m ' + url
        if is_page_blank(url):
            text += ' => \033[32;1mBlank/Vuln\033[0m'
            with open('blank_pages2.txt', 'a') as file:
                file.write(url + '\n')
        else:
            text += ' => \033[31;1mNot Blank\033[0m'
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
                                               
    Just Blank Page Scanner Using Selenium - Recode Kece Finder \n""")
    try:
        filename = raw_input("Enter the filename containing URLs: ")
        num_threads = int(raw_input("Enter the number of threads: "))
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
