"""
Course: CSE 351 
Lesson: L03 team activity
File:   team.py
Author: <Jessen Forbush>

Purpose: Retrieve Star Wars details from a server

Instructions:

- This program requires that the server.py program be started in a terminal window.
- The program will retrieve the names of:
    - characters
    - planets
    - starships
    - vehicles
    - species

- the server will delay the request by 0.5 seconds

TODO
- Create a threaded function to make a call to the server where
  it retrieves data based on a URL.  The function should have a method
  called get_name() that returns the name of the character, planet, etc...
- The threaded function should only retrieve one URL.
- Create a queue that will be used between the main thread and the threaded functions

- Speed up this program as fast as you can by:
    - creating as many as you can
    - start them all
    - join them all

"""

from datetime import datetime, timedelta
import threading
import queue
from common import *

# Include cse 351 common Python files
from cse351 import *

# global
call_count = 0


def thread_function(q):
    while True:
        url = q.get()
        if (url == None):
            break
        item = get_data_from_server(url)
        print(f'  - {item['name']}')

def get_urls(film6, kind,):
    global call_count

    urls = film6[kind]
    print(kind)
    for url in urls:
        call_count += 1
        item = get_data_from_server(url)
        print(f'  - {item['name']}')
        
def main():
    global call_count

    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    film6 = get_data_from_server(f'{TOP_API_URL}/films/6')
    call_count += 1
    print_dict(film6)
    
    # Create a queue that can be shared
    q = queue.Queue()
    
    # Create threads
    threads = []
    thread_count = 95
    for i in range (thread_count):
        t = threading.Thread(target=thread_function , args=(q,))
        threads.append(t)
    
    for url in film6['characters']:
        q.put(url)
    
    for url in film6['planets']:
        q.put(url)
        
    for url in film6['starships']:
        q.put(url)
        
    for url in film6['vehicles']:
        q.put(url)
        
    for url in film6['species']:
        q.put(url)
        
    for i in range(thread_count):
        q.put(None)
        
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
    
    # Retrieve people
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
