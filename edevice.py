import socket
import sys
import time
import subprocess
import random

host = sys.argv[1]
port = sys.argv[2]
s = socket.socket(socket.AF_INTER, socket.SOCK_STREAM)

##Missing the connection to server with big number port implementation

def main:
   


    process_list = subprocess.run(['ps', '-eo', 'comm='], capture_output=True, text=True).stdout
        
    for line in process:
        message = [line.strip(),random.randint(1,5)]
        s.send(message..encode())

##main END

if __name__ == '__main__'
    ##Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 3:
        main()
    else:
    ##Disclose correct usage of program
        print("Usage: python3 edevice.py <server_address> <port_number>")
        sys.exit(1)
