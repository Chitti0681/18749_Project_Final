import socket
import sys
import time
from datetime import datetime
import logging

'''
AF_INET-> refers to the address family IPv4
SOCK_STREAM -> connection oriented TCP protocol

'''
heartbeat_time = int(input("Enter the heartbeat rate: "))
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger("my-logger")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sGFD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket was created successfully")
except socket.error as err:
    print("Socket creation failed with error code %s" % (err))

port     = int(sys.argv[1])
port_GFD = int(sys.argv[2])
localhost = "127.0.0.1"
# localhost = "10.0.0.189"
lfd_num   = int(sys.argv[3])
# try:
#     host_ip=socket.gethostbyname('www.google.com')
# except socket.gaierror:
#     print("Error resolving the host ip")
#     sys.exit()

s.connect((localhost, port))
# localhost1 = "10.0.0.189"s
localhost1 = "127.0.0.1"

sGFD.connect((localhost1, port_GFD))

print("The socket has successfull connected to the host ip on port == %s" % (localhost))

time.sleep(heartbeat_time)
m = 0
n = 0
while True:
    try:
        message = " Are you alive?"
        s.sendall(message.encode())
        log.info("LDF sent " + message)
        rcv_message = s.recv(1024)
        log.info("From Server: "+rcv_message.decode('utf-8'))
        time.sleep(heartbeat_time)
    except:
        log.info("The Server is not responding")
        if m == 0:
            message = " LFD" + \
                str(lfd_num) + ": delete replica S" + str(lfd_num)
            log.info(" LFD sent to GFD " + message)
            sGFD.sendall(message.encode())
            n -= 1
        m += 1
        
        time.sleep(2)
        s.close()
        try:
            print("Over")
            s  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((localhost, port))
            print("Done")
        except:
            continue

    print("value of n :", n)    
    if n == 0:
        try:

            message = " LFD" + \
                str(lfd_num) + ": add replica S" + str(lfd_num)
            log.info(" LFD sent to GFD " + message)
            sGFD.sendall(message.encode())
            n += 1
            # rcv_message=sGFD.recv(1024)
            log.info(" From GFD: "+rcv_message.decode('utf-8'))
        except:
            log.info("The Server is not responding 1")
            time.sleep(2)
