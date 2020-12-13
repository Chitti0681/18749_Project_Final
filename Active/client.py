import socket
from datetime import datetime
import time
import sys

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Socket was created successfully")
except socket.error as err:
    print("Socket creation failed with error code %s" %(err))

port=int(sys.argv[3])
port1=int(sys.argv[4])
port2=int(sys.argv[5])

localhost="127.0.0.1"

'''
AF_INET-> refers to the address family IPv4
SOCK_STREAM -> connection oriented TCP protocol

'''
client_id = int(sys.argv[1])
state     = int(sys.argv[2])
s.connect((localhost,port))
s1.connect((localhost,port1))
s2.connect((localhost,port2))

print("The socket has successfull connected to the host ip on port == %s" %(localhost))


try:
    dateTimeObj    = datetime.now()
    timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    message        = "[" + timestampStr + "]"  +   " Sent <C" + str(client_id) + ", S, 101, " + str(state) + ">"
    print(" \n Client sent " + message)
    s.sendall(message.encode())
    s1.sendall(message.encode())
    s2.sendall(message.encode())
    rcv_message=s.recv(1024)
    print("\n From Server: ", rcv_message.decode('utf-8'))
except:
    print("The Server is not responding")
    time.sleep(2)
