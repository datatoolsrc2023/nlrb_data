from math import sqrt
from joblib import Parallel, delayed
from os import getpid
from scraper import case_pages_to_fetch, fetch_case_page, write_case_page
from common import Connection, paths, db_config
import concurrent.futures



def lil_printer(n):
    print(n, getpid())


parallel = Parallel(n_jobs=3)
# output_generator = parallel(delayed(lil_printer)(i) for i in range(10))

cnx = Connection(db_config)
curs = cnx.cursor()  
case_list = case_pages_to_fetch(cursor=curs)


# ok, try threading instead
import logging
import threading
import time


def thread_function(name):
    logging.info(f"Thread {name}: starting")
    time.sleep(int(name))
    logging.info(f"Thread {name}: finishing")
"""
# this one is doing a single thread, learning about daemon=True/False
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,

                        datefmt="%H:%M:%S")

    logging.info("Main  : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,), daemon=True)
    logging.info("Main  : before running thread")
    x.start()
    logging.info("Main  : wait for the thread to finish")
    # x.join()
    logging.info("Main  : all done")
"""
"""
# crude way of doing multiple threads
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    threads = list()
    for index in range(3):
        logging.info(f"Main  : create and start thread {index}.")
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()
    
    for index, thread in enumerate(threads):
        logging.info(f"Main  : before joining thread {index}.")
        thread.join()
        logging.info(f"Main  : thread {index}. done.")
"""


class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update", name)


# using the threadpoolexecutor
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, 
                        level=logging.INFO,
                        datefmt="%H:%M:%S")
    database = FakeDatabase()
    logging.info(f"Testing update. Starting value is {database.value}.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info(f"Testing update. Ending value is {database.value}.")

