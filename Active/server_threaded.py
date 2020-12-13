import sys
import time
import socket
import logging
import threading
from datetime import datetime

# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
# log = logging.getLogger("my-logger")

# current_state_glob = [0, 0, 0]
# checkPoint_flag = [0]


# class Server_Client(threading.Thread):
#     def __init__(self, serv_entity='client', port=0):
#         super(Server_Client, self).__init__()
#         self.stop = False
#         self.type = serv_entity
#         self.port = port

#     def make_client_message(self, message, message_id):
#         """ code to construct client message, pass message, message_id"""
#         # make a dateTime object
#         message_new = " Sent <C" + str(message[-13]) + ", S1, " + str(
#             message_id) + ", state changed to " + str(message[-2]) + ">"
#         return message_new

#     def run(self):
#         global current_state_glob
#         global checkPoint_flag

#         # if the checkpoint is not available, go into quiescence
#         # if checkPoint_flag[0] == 0:
#         #     time.sleep(1)
#         #     self.run()

#         current_state = [0, 0, 0]

#         # create a socket
#         s = socket.socket()

#         log.info("Socket Created Successfully.\n")

#         port = self.port

#         local_host = "127.0.0.1"

#         s.bind((local_host, port))

#         s.listen(5)

#         c, addr = s.accept()

#         # set a message id
#         message_id = 100

#         while True:
#             # get the message
#             decoded_msg = c.recv(1024).decode('utf-8')

#             log.info("Client has sent, " + decoded_msg)

#             # print the current state of the server
#             log.info("The current state is " + str(current_state) +
#                      " before processing the request \n")

#             # update the current state
#             current_state[int(decoded_msg[-13]) - 1] = int(decoded_msg[-2])

#             # print the updated state
#             log.info("The updated state is " + str(current_state) +
#                      " after processing the request\n")

#             # construct client message
#             message_new = self.make_client_message(decoded_msg, message_id)

#             message_id += 1

#             current_state_glob = current_state

#             # send the message
#             c.sendall(message_new.encode())

#             # listen for new clients
#             s.listen(5)

#             # accept the connection
#             c, addr = s.accept()


# class Server_lfd(threading.Thread):
#     def __init__(self):
#         super(Server_lfd, self).__init__()
#         self.port = int(sys.argv[4])

#     def run(self):
#         s = socket.socket()
#         log.info("New socket created for lfd..")

#         # bind the socket
#         localhost = "127.0.0.1"

#         port = self.port

#         s.bind((localhost, port))

#         s.listen(5)

#         c, addr = s.accept()

#         log.info("Connected to LFD")

#         while True:
#             try:
#                 # get the message from lfd
#                 rcv_msg = c.recv(1024).decode('utf-8')

#                 log.info("From LFD " + rcv_msg)

#                 message = 'Alive'

#                 c.sendall(message.encode())

#                 log.info("Server send Alive")

#             except:

#                 log.info("The client has stopped responding.")

#                 s.close()

#                 s = socket.socket()

#                 # bind the socket
#                 localhost = "127.0.0.1"

#                 s.bind((localhost, port))

#                 s.listen(5)

#                 c, addr = s.accept()


# class Server_Server(threading.Thread):
#     def __init__(self):
#         super(Server_Server, self).__init__()
#         self.port = int(sys.argv[2])

#     def run(self):
#         global current_state_glob
#         while True:
#             try:
#                 # make a sockey
#                 s = socket.socket()

#                 # get the port num
#                 port = self.port

#                 local_host = "127.0.0.1"

#                 # connect to the port
#                 s.connect((local_host, port))

#                 while True:
#                     try:
#                         # try to send the message
#                         message = str(current_state_glob)
#                         s.sendall(message)
#                     except:
#                         # if connection broken, close the socket
#                         s.close()
#                         break
#                     except:
#                         # go back and try again
#                         continue


# class Server_Recv(threading.Thread):
#     def __init__(self):
#         super(Server_Recv, self).__init__()
#         self.port = int(sys.argv[1])

#     def run(self):
#         global current_state_glob
#         global checkPoint_flag
#         while True:
#             try:
#                 s = socket.socket()

#                 log.info("Socket created for server")

#                 # set the port
#                 port = self.port

#                 localhost = "127.0.0.1"

#                 s.bind((localhost, port))

#                 s.listen(5)

#                 c, addr = s.accept()

#                 while True:
#                     try:
#                         rcv_msg = c.recv(1024).decode('utf-8')
#                         next_state = [int(rcv_msg[1]), int(
#                             rcv_msg[4]), int(rcv_msg[7])]
#                         for num1, num2 in zip(next_state, current_state_glob):
#                             if num1 != num2:
#                                 current_state_glob = next_state
#                                 break
#                         if checkPoint_flag[0] == 0:
#                             log.info("Checkpoint Received.")
#                             checkPoint_flag[0] = 1
#                         if rcv_msg == "":
#                             break
#                     except:
#                         s.close()
#                         break
#             except:
#                 continue


# # # main
# client_thread = Server_Client(port=int(sys.argv[3]))
# client_thread.start()

# lfd_thread = Server_lfd()
# lfd_thread.start()

# server_thread = Server_Server()
# server_thread.start()

# server_r = Server_Recv()
# server_r.start()


import threading
import time
import socket
import sys
from datetime import datetime
current_state__ = [0, 0, 0]
chkpt_flag      = [0]
print(str(current_state__))
class Sample(threading.Thread):
    def __init__(self, thread_serv_type="client", client_port = 0):
        super(Sample, self).__init__()

        self.stop = False
        self.type = thread_serv_type
        self.client_port = client_port


    def run(self):
        global current_state__
        global chkpt_flag
        if self.type == "client":
            if chkpt_flag[0] == 0:
                time.sleep(2)
                self.run()
            current_state = [0, 0, 0]
            s=socket.socket()
            print("Socket successfully created !!!")
            port = self.client_port
            localhost="127.0.0.1"
            # localhost = "10.0.0.113"
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
                current_state__ = current_state
                time.sleep(1)
                s.listen(5)
                c,addr=s.accept()

        elif self.type == "lfd":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = int(sys.argv[4])
            localhost="127.0.0.1"
            # localhost = "10.0.0.113"
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

        elif self.type == "recv":
            while True:
                try:
                    s = socket.socket()
                    # print("socket successfully created")
                    port = int(sys.argv[1])
                    localhost = "127.0.0.1"
                    s.bind((localhost, port))
                    # print("Socket is listening")
                    s.listen(5)
                    c, addr = s.accept()
                    while True:
                        try:
                            rcv_msg = c.recv(1024).decode('utf-8')
                            next_state = [int(rcv_msg[1]), int(rcv_msg[4]), int(rcv_msg[7])]
                            for num1, num2 in zip(next_state, current_state__):
                                if num1 != num2:
                                    current_state__ = next_state
                                    break
                            time.sleep(2)
                            if chkpt_flag[0] == 0:
                                print("Check point received: ", current_state__)
                                chkpt_flag[0] = 1
                            if rcv_msg == "":
                                break
                        except:
                            s.close()
                            # time.sleep(2)
                            break
                except:
                    # time.sleep(2)
                    continue

        elif self.type == "recv1":
            while True:
                try:
                    s = socket.socket()
                    # print("socket successfully created")
                    # port = int(sys.argv[2])
                    localhost = "127.0.0.1"
                    s.bind((localhost, port))
                    # print("Socket is listening")
                    s.listen(5)
                    c, addr = s.accept()
                    while True:
                        try:
                            rcv_msg = c.recv(1024).decode('utf-8')
                            current_state__ = int(rcv_msg)
                            print("HELLO")
                            print(current_state__)
                            print(rcv_msg)
                            if rcv_msg == "":
                                break
                        except:
                            s.close()
                            time.sleep(2)
                            break
                except:
                    time.sleep(2)
                    continue

        elif self.type == "serv":
            while True:
                try:
                    s = socket.socket()
                    port = int(sys.argv[2])
                    localhost = "127.0.0.1"
                    s.connect((localhost, port))
                    while True:
                        try:
                            message = str(current_state__)
                            # print(message)
                            time.sleep(2)
                            s.sendall(message.encode())
                        except:
                            s.close()
                            time.sleep(2)
                            break
                except:
                    time.sleep(2)
                    continue


        elif self.type == "serv1":
            while True:
                try:
                    s = socket.socket()
                    # port = int(sys.argv[4])
                    localhost = "127.0.0.1"
                    s.connect((localhost, port))
                    while True:
                        try:
                            message = str(current_state__)
                            # print(message)
                            time.sleep(2)
                            s.sendall(message.encode())
                        except:
                            s.close()
                            time.sleep(2)
                            break
                except:
                    time.sleep(2)
                    continue


    def test(self):
        print('testing... client')
        time.sleep(2)

    def test2(self):
        print("Testing .. lfd")
        time.sleep(2)


# main
sample = Sample(client_port=int(sys.argv[3]))
sample.start()      # Initiates second thread which calls sample.run()
sample.test()       # Main thread calls sample.test

# sample5 = Sample(client_port=10115)
# sample5.start()      # Initiates second thread which calls sample.run()
# # sampl.test()       # Main thread calls sample.test

# sample5 = Sample(client_port=10116)
# sample5.start()      # Initiates second thread which calls sample.run()
# # sample.test()       # Main thread calls sample.test
# # sample.stop=True    # Main thread sets sample.stop
# # sample.join()       # Main thread waits for second thread to finish

sample2 = Sample("lfd")
sample2.start()
sample2.test2()

sample3 = Sample("serv")
sample3.start()
# time.sleep(2)

# sample3 = Sample("serv1")
# sample3.start()
# time.sleep(2)
# sample2.test2()
sample4 = Sample("recv")
sample4.start()
# # sample2.test2()
# sample4 = Sample("recv1")
# sample4.start()
