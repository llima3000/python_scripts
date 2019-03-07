import datetime
import socket
import time
import sys

if len(sys.argv) != 2:
    print("Wrong parameters. Use: ")
    print("   %s <IP ADDRESS>" % sys.argv[0])
    exit(-255)

HOST = sys.argv[1]

PORT = 50000
BUFFER = 1024
count = 0
size = -1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

sock.send("Hi!".encode('utf-8'))
time.sleep(1)

data = sock.recv(BUFFER)

if data != b'':
    size = int(str(data.decode('utf-8')))
else:
    print("empty response")
    exit(-1)

print("Test data size is: %f GB" % (size))

if size > 0:
    starttime = datetime.datetime.now()
    while count < size:
        data = sock.recv(BUFFER)
        if data:
            #print_there(10, 10, str(count))
            count += len(data)
            del data
        else:
            break
            
response = ""
data = b''
time.sleep(1)
while True:
    tmp = sock.recv(BUFFER)
    if tmp:
        data += tmp
        del tmp

    else:
        break

sock.close()
response = data.decode('utf-8')
print(response)