# Code to do network test with python
#from __future__ import print_function

import datetime
import socket
import _thread
import sys

HOST = '0.0.0.0'
PORT = 50000
BUFFER = 1024
threadcount = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(0)
print('listening at %s:%s\n\r' %(HOST, PORT))

def print_there(threadnum,text):
    #sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.write("\x1b7\x1b[%dD%s\x1b8" % (threadnum * 12, text))
    sys.stdout.flush()

# Define a function for the thread
def process_connection(threadNumber, clisock, cliaddr):
    global threadcount
    count = 0
    size = -1
    print("Thread %d started, socket %d" %(threadNumber, clisock.fileno()))

    data = clisock.recv(BUFFER)
    if data != b'':
        size = int(str(data.decode('utf-8')))

    if size > 0:
        starttime = datetime.datetime.now()
        while count < size:
            data = clisock.recv(BUFFER)
            if data:
                #print_there(10, 10, str(count))
                count += len(data)
                del data
            else:
                break
            
        endtime = datetime.datetime.now()
        response = str(endtime) + "\n\r"
        response = response + ('\n\r%s:%s disconnected\n\r' % cliaddr)
        response = response + ('GB transferred: %f(0.1)' % (count/1024/1024/1024) + "\n\r")
        delta = endtime - starttime
        delta = delta.seconds + delta.microseconds / 1000000.0
        response = response + ('time used (seconds): %f' % delta) + "\n\r"
        response = response + ('averaged speed (MB/s): %f\n\r' % (count / 1024 / 1024 / delta)) + "\n\r"

        try:
            clisock.send(response.encode('utf-8'))
            print(response)

        except:
            pass
    
    print("Thread %d stoped, closing socket %d" % (threadNumber, clisock.fileno()))
    clisock.close()
    threadcount -= 1


while True:

    client_sock, client_addr = sock.accept()
    try:
        _thread.start_new_thread(process_connection, (threadcount, client_sock, client_addr))
        threadcount += 1

    except:
        print("Error: unable to start thread")

sock.close()
