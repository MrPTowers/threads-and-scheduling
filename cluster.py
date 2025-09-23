import threading
import time
import socket
import sys

host = '127.0.0.1'
port = int(sys.argv[1]) #Program parameters
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Initizalize socket for TCP connection
queue_max = 10
queue = []
lock = threading.Lock() #Protection of critical regions
empty_slots = threading.Semaphore(queue_max) #Semaphore to represent empty places in queue
full_slots = threading.Semaphore(0) #Semaphore to represent amount of jobs in queue

proc_tables = {} #Dictionary to store executed processes per thread
execution_times = {} #Dictionaru to store total execution time per thread
producer_done = False #Flag to detemine once producer has finished

def consumer(thread_id):
    proc_table = [] #Local array for executed processes
    execution_time = 0 #Accumulator for total execution time
    while True:
        full_slots.acquire() #Down full slots. Locks if queue is empty
        
        lock.acquire() #Critical region start
        if queue: #Enters unless queue is empty
            process = queue.pop(0) #Remove first process in queue
            lock.release() #Critical region end
            print(f"Consumer {thread_id} ran {process[0]}")
            empty_slots.release() #Up empty slot
            proc_table.append(process) #Append and add to local variables
            execution_time += process[1]
            time.sleep(process[1]) #Sleep for execution time
        else:
            if producer_done: #If queue empty, check if producer is done
                lock.release() #Critical region end and leave While loop
                break
            lock.release() #Critical region end
            full_slots.release() #Nothing was consumed. Return semaphore to prior state

    proc_tables[thread_id] = proc_table #At execution end, append to dictionaries based on thread_id
    execution_times[thread_id] = execution_time

#consumer END

def producer(clientSocket):    
    while True:
        msg = clientSocket.recv(1024).decode() #Receive incomming message
        if not msg or msg == 'done': #If edevice sends 'done', break from loop
            break
        parts = msg.split(',') #Split string in 2: Process name and execution time
        job = [parts[0], int(parts[1])]
        empty_slots.acquire() #Down empty slots
        lock.acquire() #Critical region start
        queue.append(job) #Append to queue and sort
        queue.sort(key=shortestJobFirst)
        lock.release() #Critical region end
        full_slots.release() #Up full slots.
        time.sleep(job[1])
    global producer_done
    lock.acquire() #Critical region start (Signal completion)
    producer_done = True #After loop ends, change flag to true
    lock.release() #Critical region end
    print("Producer finished sending jobs.")
    for i in range(2): #Wake up consumers. Hard-coded to 2 due to the number of consumers
        full_slots.release() 

#producer END

def shortestJobFirst(e):
    return e[1] #Return second element of the tuple (execution time)

# shortestJobFirst END

def main():
    s.bind((host,port)) 
    s.listen() #Bind server to host and port and start listening for connection
    print(f"Server listening on  {host}:{port}")

    clientSocket, address = s.accept()
    print(f"Connection established from address {address}") 

    threads = [] #Threads array

    c1 = threading.Thread(name='c1', target=consumer, args=(1,))
    c2 = threading.Thread(name='c2', target=consumer, args=(2,))
    p = threading.Thread(name='p', target=producer, args=(clientSocket,))

    threads.append(c1)
    threads.append(c2)
    threads.append(p)

    for t in threads: #After appending, start all threads
        t.start()

    for t in threads: #Wait for threads to finish
        t.join()

    results = ""
    for cid, table in proc_tables.items(): #Parse proc_tables and execution_times into message
        results+= f"Consumer {cid} processed:\n"
        for job in table:
            results += f"{job[0]},{job[1]}\n"
        results += f"Consumer {cid} spent {execution_times[cid]} seconds of CPU time\n"
        results += "---\n"



    clientSocket.sendall(results.encode()) #Send message back to edevice.
    clientSocket.close()
    s.close() #Close both connections

#main END


if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 2:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 cluster.py <port_number>")
        sys.exit(1)

