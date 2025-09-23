import socket
import sys
import subprocess
import random
import time

host = sys.argv[1]
port = int(sys.argv[2]) #Program parameters
execution_time_range = [1,5]
sleep_time_range = [1,5]

def main(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port)) #Connect to server with TCP connection
    
    process_list = subprocess.run(['ps', '-eo', 'comm='], capture_output=True, text=True).stdout.splitlines() #Collect names of all running processes

    for line in process_list: #Send individual message for each line in process_list
        msg = f"{line.strip()},{random.randint(sleep_time_range[0],sleep_time_range[1])}"
        s.send(msg.encode())
        time.sleep(random.randint(execution_time_range[0],execution_time_range[1]))

    time.sleep(5)
    s.send("done".encode()) #Send final message to indicate end
    while True:
        data = s.recv(16384) #Receive and display final result
        if not data:
            continue
        print(f"\nMessage received:\n {data.decode()}")
        break

    s.close() #Close connection

##main END

if __name__ == '__main__':
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 3:
        main()
    else:
    #Disclose correct usage of program
        print("Usage: python3 edevice.py <server_address> <port_number>")
        sys.exit(1)
