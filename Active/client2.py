import threading
import time
import socket
import sys
from datetime import datetime


class Sample(threading.Thread):
    def __init__(self, thread_serv_type, state, message_id, s_count):
        super(Sample, self).__init__()

        self.stop = False
        self.type = thread_serv_type
        self.state = state
        self.message_id = message_id
        self.s_count = s_count

    def prints(self, message):
        lock.acquire()
        print(message)
        lock.release

    def run(self):
        client_id = int(sys.argv[1])

        # state = (int)(input("Enter the state between 0 and 5 : "))

        if self.type == "s1":

            try:
                s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print(
                    "Socket creation failed with error code %s" % (err))

            port1 = 10113
            localhost1 = "127.0.0.1"

            '''
            AF_INET-> refers to the address family IPv4
            SOCK_STREAM -> connection oriented TCP protocol

            '''
            try:
                s1.connect((localhost1, port1))
                # print("The socket has successfull connected to the Server 1 on port == %s" % (
                #     localhost1))
            except:
                print("S1 Down")

            try:
                dateTimeObj    = datetime.now()
                timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                message        = "[" + timestampStr + "]"  +   " Sent <C" + str(client_id) + ", S, 101, " + str(state) + ">"
                print(" \n Client sent " + message)
                s1.sendall(message.encode())
                rcv_message=s1.recv(1024)
                print("\n From Server: ", rcv_message.decode('utf-8'))
            except:
                print("The Server is not responding")
                time.sleep(2)

        elif self.type == "s2":

            try:
                s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print(
                    "Socket creation failed with error code %s" % (err))

            port2 = 10114
            localhost2 = "127.0.0.1"
            # localhost2 = "10.0.0.189"

            '''
            AF_INET-> refers to the address family IPv4
            SOCK_STREAM -> connection oriented TCP protocol

            '''
            try:
                s2.connect((localhost2, port2))
            except:
                print("S2 Down")

            try:
                dateTimeObj    = datetime.now()
                timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                message        = "[" + timestampStr + "]"  +   " Sent <C" + str(client_id) + ", S, 101, " + str(state) + ">"
                print(" \n Client sent " + message)
                s2.sendall(message.encode())
                rcv_message=s2.recv(1024)
                print("\n From Server: ", rcv_message.decode('utf-8'))
            except:
                print("The Server is not responding")
                time.sleep(2)

        elif self.type == "s3":

            try:
                s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print(
                    "Socket creation failed with error code %s" % (err))

            port3 = 10115
            localhost3 = "127.0.0.1"

            '''
            AF_INET-> refers to the address family IPv4
            SOCK_STREAM -> connection oriented TCP protocol

            '''
            try:
                s3.connect((localhost3, port3))
            except:
                print("S3 Down")

            try:
                dateTimeObj    = datetime.now()
                timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                message        = "[" + timestampStr + "]"  +   " Sent <C" + str(client_id) + ", S, 101, " + str(state) + ">"
                print(" \n Client sent " + message)
                s3.sendall(message.encode())
                rcv_message=s3.recv(1024)
                print("\n From Server: ", rcv_message.decode('utf-8'))

            except:
                print("The Server is not responding")
                time.sleep(2)


message_id = int(sys.argv[2])
state = 2
s_count = [0, 0, 0]
lock = threading.Lock()
while (True):
    # main

    
    # state = (int)(input("Enter the state between 0 and 5 : "))
    state = (state + 1) % 5
    message_id += 1
    sample = Sample("s1", state, message_id, s_count)
    sample.start()      # Initiates second thread which calls sample.run()

    sample2 = Sample("s2", state, message_id, s_count)
    sample2.start()

    sample3 = Sample("s3", state, message_id, s_count)
    sample3.start()

    sample.join()
    sample2.join()
    sample3.join()

    s_decimal = 1*s_count[0] + 2*s_count[1] + 4*s_count[2]

    if (s_decimal == 3):
        print(str(message_id) + " Discarded duplicate reply from S2")
    elif (s_decimal == 5):
        print(str(message_id) + " Discarded duplicate reply from S3")
    elif (s_decimal == 6):
        print(str(message_id) + " Discarded duplicate reply from S3")
    elif (s_decimal == 7):
        print(str(message_id) + " Discarded duplicate reply from S2\n" +
              str(message_id) + " Discarded duplicate reply from S3")

    s_count = [0, 0, 0]
    time.sleep(10)
