import threading
import time
import socket
import sys
from datetime import datetime

req_num = []

class Sample(threading.Thread):
    def __init__(self, thread_serv_type="client"):
        super(Sample, self).__init__()

        self.stop = False
        self.type = thread_serv_type

    def run(self):
        if self.type == "client":
            current_state = [0, 0, 0]
            s=socket.socket()
            print("Socket successfully created !!!")
            port = 10108
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))

            s.listen(5)
            print("Socket is listening")

            c,addr=s.accept()
            print("Got connnection from ", addr)
            while True:
                dateTimeObj  = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                rcv_msg      = c.recv(1024)
                print("Client has sent: ", rcv_msg.decode('utf-8'))

                print("My current state ", current_state, " before processing the request\n")
                current_state[int(rcv_msg.decode('utf-8')[-13]) - 1] = int(rcv_msg.decode('utf-8')[-2])
                print("My current state ", current_state, "  after processing request\n")

                dateTimeObj    = datetime.now()
                timestampStr   = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                message        = "[" + timestampStr + "]"  +   " Sent <C" + str(rcv_msg.decode('utf-8')[-13]) + ", S1, 101, " + "state changed to " + str(rcv_msg.decode('utf-8')[-2]) +">"
                print("Sending ", message)
                c.sendall(message.encode())
                time.sleep(1)
                s.listen(5)
                c,addr=s.accept()
        else if self.type == "lfd":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = 10109
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))
            s.listen(5)
            print("Socket is listening")
            c,addr=s.accept()
            print("Got connnection from ", addr)
            while True:
                try:
                    dateTimeObj  = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    rcv_msg      = c.recv(1024)
                    print("From LDF: ",rcv_msg.decode('utf-8'))
                    message=timestampStr + ' Alive'
                    c.sendall(message.encode())
                    print(timestampStr+'Server sent Alive')
                except:
                    print("The client has stopped responding")
                    time.sleep(2)
                    s.listen(5)
                    print("Socket is listening")
                    c,addr=s.accept()
        else if self.type == "active_send1":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = 10109
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))
            s.listen(5)
            print("Socket is listening")
            c,addr=s.accept()
            print("Got connnection from ", addr)

            while True:
                try:
                    rcv_msg      = c.recv(1024)
                    message      = "Alive"
                    c.sendall(message.encode())
                    print('Server sent Alive')
                except:
                    print("The server has died, logging requests")
                    time.sleep(2)
                    s.listen(5)
                    self.run()

        else if self.type == "active_send2":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = 10109
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))
            s.listen(5)
            print("Socket is listening")
            c,addr=s.accept()
            print("Got connnection from ", addr)

            while True:
                try:
                    rcv_msg      = c.recv(1024)
                    message      = "Alive"
                    c.sendall(message.encode())
                    print('Server sent Alive')
                except:
                    print("The server has died, logging requests")
                    time.sleep(2)
                    s.listen(5)
                    self.run()
        else if self.type == "active_recv":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = 10109
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))
            s.listen(5)
            print("Socket is listening")
            c,addr=s.accept()
            print("Got connnection from ", addr)

            while True:
                try:
                    rcv_msg      = c.recv(1024)
                    message      = "Alive"
                    c.sendall(message.encode())
                    print('Server sent Alive')
                except:
                    print("The server has died, logging requests")
                    time.sleep(2)
                    s.listen(5)
                    self.run()

#main
sample = Sample()
sample.start()      # Initiates second thread which calls sample.run()
sample.test()       # Main thread calls sample.test
# sample.stop=True    # Main thread sets sample.stop
# sample.join()       # Main thread waits for second thread to finish

sample2 = Sample("lfd")
sample2.start()
sample2.test2()

sample3 = Sample("active_send1")
sample3.start()
sample3.test2()

sample4 = Sample("active_send2")
sample4.start()
sample4.test2()