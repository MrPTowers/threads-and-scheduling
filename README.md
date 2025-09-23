# threads-and-scheduling
 Pablo Torres Arroyo
 801-19-7744
 23/09/2025


### Libraries used:
---
1. **Threading**: Threads, locks, and semaphores
2. **Subprocess**: Run terminal commands
3. **Time**: Sleep library
4. **Random**: Randomization for sleep times
5. **Socket**: Server setup and client-server communication
6. **Sys**: Capture program parameter

### How to Run
---

The project consists of two separate programs:

- cluster.py:

Use: python3 cluster.py <server_port>

The program acts as a server that will wait for messages from an embedded device.
The messages are a tuple consisting of process name and execution time for said process.

It creates one producer thread that acts as a scheduler. It receives the message, parses it
for execution and sorts all current scheduled processes by a Shortest Job First algorithm.

The program also creates two consumer threads that "execute" the processes and sleeps for
the execution time provided by the embedded device.

Once the threads finish, the cluster sends a message back to the embedded device that states
which processes were "executed" and the total amount of execution time for each consumer.

-The server address used is 127.0.0.1-

- edevice.py

Use: python3 edevice.py <server_address> <server_port>

The program acts as an embedded device that will connect to the specified server on the 
designated port It runs the terminal command ```ps -eo comm=``` and stores the result. The 
result is then iterated through and each line (process name) is stringified as a tuple with 
a randomized execution time. Each tuple is sent to the cluster individually.

After all processes are sent, the embedded device sends a message declaring that is has
finished and waits to receive the response of the finished execution.

### Sources consulted
---
People:
1. Uriel Fuentes: Offered insight edevice message parsing and subprocess library use
2. Gabriel Roman: Explained semaphore use cases for the project

Online:
1. https://stackoverflow.com/questions/7749341/basic-python-client-socket-example
Based the initial socket server setup on this.
2. https://www.geeksforgeeks.org/python/synchronization-by-using-semaphore-in-python/
Learned basic python threading syntax
3. https://docs.python.org/3/library/subprocess.html#subprocess.Popen
Informed the usage of the subprocess library
