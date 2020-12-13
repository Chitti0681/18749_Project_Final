# import threading
# import time
# import socket
# import sys
# from datetime import datetime
# import logging


# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
# log = logging.getLogger("my-logger")


# port1 = int(sys.argv[1])
# # port2 = int(sys.argv[2])
# # port3 = int(sys.argv[3])

# RM_MEMBERS = [0, 0, 0]
# RM_MEM_COUNT = [0]
# current_state = [1, 1, 1]


# class Sample(threading.Thread):
#     def __init__(self, thread_serv_type="gfd", port_num=10110):
#         super(Sample, self).__init__()

#         self.stop = False
#         self.type = thread_serv_type
#         self.port_num = port_num

#         self.gfd_num = 0

#     def run(self):
#         if self.type == "gfd":
#             s = socket.socket()
#             print("Socket successfully created !!!")
#             port = self.port_num
#             # localhost="127.0.0.1"
#             localhost = "10.0.0.189"
#             s.bind((localhost, port))
#             print("Socket bound to %s" % (port))

#             s.listen(10)
#             print("Socket is listening")
#             c, addr = s.accept()

#             while True:

#                 # print("Before")
#                 # rcv_msg = c.recv(1024)
#                 # print("After")
#                 # log.info("RM: " + rcv_msg.decode('utf-8'))
#                 try:
#                     # print("Before")
#                     rcv_msg = c.recv(1024)
#                     # print("After")
#                     log.info("RM: " + rcv_msg.decode('utf-8'))

#                 except:

#                     time.sleep(1)
#                     print("GFD" + " is not responding.")

#                 # c.close()
#                     # run()


# # main
# sample = Sample(port_num=port1)
# sample.start()      # Initiates second thread which calls sample.run()
# # sample.test()       # Main thread calls sample.test

# # sample1 = Sample(port_num=port2)
# # sample1.start()
# # # sample1.test2()

# # sample2 = Sample(port_num=port3)
# # sample2.start()
# # # sample2.test2()


import threading
import time
import socket
import sys
from datetime import datetime
import subprocess

port1 = int(sys.argv[1])
port2 = int(sys.argv[2])
port3 = int(sys.argv[3])

mode = sys.argv[4]

RM_MEMBERS = [0, 0, 0]
RM_MEM_COUNT = [0]
current_state = [1, 1, 1]
primary = [0]


class Sample(threading.Thread):
    def __init__(self, thread_serv_type="gfd", port_num=10111):
        super(Sample, self).__init__()

        self.stop = False
        self.type = thread_serv_type
        self.port_num = port_num

        self.gfd_num = 0

    def run(self):
        if self.type == "gfd":
            s = socket.socket()
            print("Socket successfully created !!!")
            port = self.port_num
            # localhost="127.0.0.1"
            localhost = "10.0.0.189"
            s.bind((localhost, port))
            print("Socket bound to %s" % (port))

            s.listen(5)
            print("Socket is listening")

            c, addr = s.accept()
            print("Got connnection from ", addr)

            try:
                s_change = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket was created successfully")
            except socket.error as err:
                print("Socket creation failed with error code %s" % (err))

            while True:

                try:
                    rcv_msg = c.recv(2046)
                    # print("lfd has sent: ", rcv_msg.decode('utf-8'))
                    a = rcv_msg.decode('utf-8')
                    print("RM: " + str(a))

                    status = a[-5]
                    count = int(a[0])
                    if status != "A":
                        RM_MEMBERS[0] = RM_MEMBERS[1] = RM_MEMBERS[2] = 0

                    if count == 1:
                        RM_MEMBERS[int(a[10])-1] = 1
                        primary[0] = 1
                    elif count == 2:
                        RM_MEMBERS[int(a[11])-1] = 1
                        RM_MEMBERS[int(a[15])-1] = 1
                    elif count == 3:
                        RM_MEMBERS[int(a[11])-1] = 1
                        RM_MEMBERS[int(a[15])-1] = 1
                        RM_MEMBERS[int(a[19])-1] = 1

                    if (RM_MEMBERS[0] == 0 and RM_MEMBERS[1] != 0) and primary[0] == 1:
                        # print("in")
                        port = 12345
                        localhost = "10.0.0.189"
                        s_change.connect((localhost, port))
                        message = "0 10116 10121 10120"
                        if mode == 'a':
                            subprocess.call(['sh', './Backup1.sh'])
                        s_change.sendall(message.encode())
                        primary[0] = 2

                    if mode == 'a':
                        if (RM_MEMBERS[0] == 0 and RM_MEMBERS[1] != 0) and primary[0] == 2:
                            subprocess.call(['sh', './Backup1.sh'])
                        elif (RM_MEMBERS[2] == 0 and RM_MEMBERS[1] != 0) and primary[0] == 2:
                            subprocess.call(['sh', './Backup2.sh'])

                        if status != "A":
                            if (RM_MEMBERS[0] != 0 and RM_MEMBERS[1] == 0 and RM_MEMBERS[2] != 0) and primary[0] == 1:
                                subprocess.call(['sh', './Backup1_Before.sh'])
                            elif (RM_MEMBERS[0] != 0 and RM_MEMBERS[1] != 0 and RM_MEMBERS[2] == 0) and primary[0] == 1:
                                subprocess.call(['sh', './Backup2_Before.sh'])
                except:
                    time.sleep(10)
                    print("GFD" + " is not responding.")
                    self.run()
            # s.close()
            # self.run()


# main
sample = Sample(port_num=port1)
sample.start()

sample2 = Sample(port_num=port2)
sample2.start()

sample3 = Sample(port_num=port3)
sample3.start()
