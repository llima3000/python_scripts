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
BUFFER = 1024 * 4
RANGE = 1024*1024

testdata = b''
for i in range(0, BUFFER):
    testdata += str(i%10).encode('utf-8')

print("Test data size is: %f GB" % (len(testdata)*RANGE/1024/1024/1024))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print(str(len(testdata)*RANGE).encode('utf-8'))
sock.send(str(len(testdata)*RANGE).encode('utf-8'))
time.sleep(1)
for i in range(0, RANGE):
    sock.send(testdata)

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