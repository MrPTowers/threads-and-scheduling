import threading
import time
import socket
import sys

host = '127.0.0.1'
port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
queue_max = 10
queue = []
lock = threading.Lock()
empty_slots = threading.Semaphore(queue_max)
full_slots = threading.Semaphore(0)

proc_tables = {}
producer_done = threading.Event()

def consumer(thread_id):
    proc_table = []
    while True:
        lock.acquire() #Critical region start
        if not queue and producer_done.is_set():
            lock.release()
            break
        lock.release()
        full_slots.acquire()
        
        lock.acquire()
        if queue:
            process = queue.pop(0)
            print(f"Consumer {thread_id} ran {process[0]}")
        else:
            lock.release()
            full_slots.release()
            continue
        lock.release() #Critical region end
        
        empty_slots.release()
        proc_table.append(process)
        time.sleep(process[1])
    proc_tables[thread_id] = proc_table

#consumer END

def producer(clientSocket):    
    while True:
        msg = clientSocket.recv(1024).decode()
        if not msg or msg == 'done':
            break
        parts = msg.split(',')
        job = [parts[0], int(parts[1])]
        empty_slots.acquire()
        lock.acquire() #Critical region start
        queue.append(job)
        queue.sort(key=shortestJobFirst)
        lock.release() #Critical region end
        full_slots.release()
        time.sleep(0.5)
    producer_done.set()
    print("Producer finished sending jobs.")

#producer END

def shortestJobFirst(e):
    return e[1] #Return second element of the tuple (execution time)


def main():
    s.bind((host,port))
    s.listen() 
    print(f"Server listening on  {host}:{port}")

    clientSocket, address = s.accept()
    print(f"Connection established from address {address}") 

    threads = []

    c1 = threading.Thread(name='c1', target=consumer, args=(1,))
    c2 = threading.Thread(name='c2', target=consumer, args=(2,))
    p = threading.Thread(name='p', target=producer, args=(clientSocket,))

    threads.append(c1)
    threads.append(c2)
    threads.append(p)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    results = ""
    for cid, table in proc_tables.items():
        results+= f"Consumer {cid} processed:\n"
        for job in table:
            results += f"{job[0]},{job[1]}\n"
        results += "---\n"

    clientSocket.sendall(results.encode())
    clientSocket.close()
    s.close()

#main END


if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 2:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 cluster.py <port_number>")
        sys.exit(1)

