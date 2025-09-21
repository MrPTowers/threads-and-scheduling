import socket
import sys
import time
import subprocess
import random

host = sys.argv[1]
port = sys.argv[2]
s = socket.socket(socket.AF_INTER, socket.SOCK_STREAM)

def isOpen:
    try:
        s.settimeout(1)

        result = s.connect_ex((host, port))

        if result == 0:    
            print(f"Successfully connected to {host}:{port}. Port is open")
            return True
        else:
            print("Error: Port is currently in use or unreachable. Error code: {result}")
            return False
    except socket.error:
        print(f"Socket error: {socket.error}")
        return False
##isOpen END

def main:
    if not 49152 <= port <= 65535:
        print("Error: Port must be between 49152 and 65535")
        sys.exit(1)
    else if (isOpen()):
        message = []
        process_list = subprocess.run(['ps', '-eo', 'comm='], capture_output=True, text=True).stdout
        
        for line in process:
            message.append([line.strip(),random.randint(1,7)])
        

        s.send(message.encode())
    else:
        sys.exit(1)

##main END

if __name__ == '__main__'
    ##Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 3:
        main()
    else:
    ##Disclose correct usage of program
        print("Usage: python3 edevice.py <server_address> <port_number>")
        sys.exit(1)
