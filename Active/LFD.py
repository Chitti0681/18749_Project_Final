import socket
import sys
import time
from datetime import datetime

'''
AF_INET-> refers to the address family IPv4
SOCK_STREAM -> connection oriented TCP protocol

'''
heartbeat_time=int(input("Enter the heartbeat rate: "))
try:
    s    = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sGFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Socket was created successfully")
except socket.error as err:
    print("Socket creation failed with error code %s" %(err))

port      = int(sys.argv[1])
port_GFD  = int(sys.argv[2])
# localhost = "127.0.0.1"
localhost = "10.0.0.113"
lfd_num = int(sys.argv[3])
# try:
#     host_ip=socket.gethostbyname('www.google.com')
# except socket.gaierror:
#     print("Error resolving the host ip")
#     sys.exit()

s.connect((localhost, port))
sGFD.connect((localhost, port_GFD))

print("The socket has successfull connected to the host ip on port == %s" %(localhost))

time.sleep(heartbeat_time)
m = 0
n = 0
while True:
    try:
        dateTimeObj  = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        message      = timestampStr+" \nAre you alive?"
        s.sendall(message.encode())
        print("LDF sent " + message)
        rcv_message  = s.recv(1024)
        print("From Server: ", rcv_message.decode('utf-8'))
        time.sleep(heartbeat_time)
    except:
        print("The Server is not responding jack")
        if m == 0:
            dateTimeObj    = datetime.now()
            timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            message        = "[" + timestampStr + "]"  +   " LFD" + str(lfd_num) +  ": delete replica S" + str(lfd_num)
            print(" \n LFD sent to GFD " + message)
            sGFD.sendall(message.encode())
        m += 1
        time.sleep(2)
        s.close()
        try:
            # print("Over")
            s  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((localhost, port))
            # print("Done")
        except:
            continue
    
    if n == 0:
        try:
            dateTimeObj    = datetime.now()
            timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            message        = "[" + timestampStr + "]"  +   " LFD" + str(lfd_num) +  ": add replica S" + str(lfd_num)
            print(" \n LFD sent to GFD " + message)
            sGFD.sendall(message.encode())
            # rcv_message=sGFD.recv(1024)
            print("\n From GFD: ", rcv_message.decode('utf-8'))
        except:
            print("The Server is not responding")
            time.sleep(2)

        n += 1
    