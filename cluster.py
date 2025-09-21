import threading
import time
import socket
import sys

#host = '127.0.0.1'
#port = sys.argv[1]
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
queue = []
lock = threading.lock()
semaphore = threading.Semaphore(value=2)



def consumer():
	proc_table = []
	while True:
		lock.acquire() ##Critical region start
		process = queue[0]
		queue.pop(1)
		lock.release() ##Critical region end
		proc_table.append(process)
		time.sleep(process[1])

##consumer END

def producer(): 
    while True:
        
        ##Listen for message
        ##Store the tuple in queue
        queue.sort(key=shortestJobFirst())

##producer END

def shortestJobFirst(e):
    return e[1] ##Return second element of the tuple (execution time)


def main():
    #s.bind(host,port)
    #s.listen(5)

        #while True
            #clientSocket, address = s.accept()
            #print(f"Connection estavlished from address {address}")    

    threads = []

    c1 = threading.Thread(name='c1', target=consumer, args=(i,))
    c2 = threading.Thread(name='c2', target=consumer, args=(i,))
    p = threading.Thread(name='p', target=producer, args=(i,))

    threads.append(c1)
    threads.append(c2)
    threads.append(p)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    #else:
     #   sys.exit(1)
      #  socket.close()

##main END


if __name__ == "__main__":
    ##Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 2:
    	main(port)
    else:
    	##Disclose correct usage of program
        print("Usage: python3 cluster.py <port_number>")
        sys.exit(1)

