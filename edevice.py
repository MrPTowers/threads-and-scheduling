import socket
import sys
import subprocess
import random
import time

host = sys.argv[1]
port = int(sys.argv[2])

def main(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    process_list = subprocess.run(['ps', '-eo', 'comm='], capture_output=True, text=True).stdout.splitlines()

    for line in process_list:
        msg = f"{line.strip()},{random.randint(1,5)}"
        print(msg)
        s.send(msg.encode())
        time.sleep(1)

    time.sleep(5)
    s.send("done".encode())
    while True:
        data = s.recv(1024)
        if not data:
            continue
        print(f"\nMessage received:\n {data.decode()}")
        break

    s.close()

##main END

if __name__ == '__main__':
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 3:
        main()
    else:
    #Disclose correct usage of program
        print("Usage: python3 edevice.py <server_address> <port_number>")
        sys.exit(1)
