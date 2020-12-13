import threading
import time
import socket
import sys
from datetime import datetime
import logging


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger("my-logger")

port1 = int(sys.argv[1])
port2 = int(sys.argv[2])
port3 = int(sys.argv[3])

GFD_MEMBERS   = [0, 0, 0]
GFD_MEM_COUNT = [0]
current_state = [1, 1, 1]
mutex = threading.Lock()
class Sample(threading.Thread):
    def __init__(self, thread_id,rm_num, thread_serv_type="lfd", port_num=10110):
        super(Sample, self).__init__()

        self.stop     = False
        self.type     = thread_serv_type
        self.port_num = port_num
        self.port_num_rm = rm_num
        self.thread_id = thread_id
        self.lfd_num  = 0

    def run(self):
        if self.type == "lfd":

            # connect to the RM
            try:
                s_rm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket was created successfully")
            except socket.error as err:
                print("Socket creation failed with error code %s" % (err))

            port = self.port_num_rm
            # localhost="127.0.0.1"
            localhost = "10.0.0.189"
            s_rm.connect((localhost,port))
            print("Socket bound to %s" %(port))

            # connect with the LFDs
            s=socket.socket()
            print("Socket successfully created !!!")
            port = self.port_num
            # localhost="127.0.0.1"
            localhost = "10.0.0.189"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))

            s.listen(5)
            print("Socket is listening")

            c,addr=s.accept()
            print("Got connnection from ", addr)


            while True:

                try:
                    rcv_msg      = c.recv(1024)
                    # print("lfd has sent: ", rcv_msg.decode('utf-8'))      
                    try:
                        # a = int(rcv_msg.decode('utf-8')[-17]) 
                        if int(rcv_msg.decode('utf-8')[-17]) == int(rcv_msg.decode('utf-8')[-1]):
                            GFD_MEMBERS[int(rcv_msg.decode('utf-8')[-1]) - 1] = 1
                            self.lfd_num = int(rcv_msg.decode('utf-8')[-1])
                            GFD_MEM_COUNT[0] += 1
                            idx = []
                            n   = 0
                            for i,mem in enumerate(GFD_MEMBERS):
                                if mem == 1:
                                    idx.append(n + 1)
                                n += 1
                            # print("Idx value : ",idx)
                            if len(idx) == 1:
                                log.info("GFD: 1 member " + "S" + str(idx[0]))
                                message        = "1 member " + "S" + str(idx[0]) +" ,1 Added"
                            elif len(idx) == 2:
                                log.info("GFD: 2 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) )
                                message        = "2 members " + "S" + str(idx[0]) + ", S" + str(idx[1])+" ,1 Added"
                            elif len(idx) == 3:
                                log.info("GFD: 3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2]))
                                message        = "3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2]) +" ,1 Added"

                            # s_rm.send(message.encode())
                            # print("sent")
                            
                    except:
                        # print("lfd has sent: ", rcv_msg.decode('utf-8'))
                        GFD_MEM_COUNT[0] -= 1
                        GFD_MEMBERS[int(rcv_msg.decode('utf-8')[-1]) - 1] = 0
                        idx = []
                        n   = 0
                        for i,mem in enumerate(GFD_MEMBERS):
                            if mem == 1:
                                idx.append(n + 1)
                            n += 1
                        if len(idx) == 0:
                            log.info("GFD: 0 members")
                            message        = "0 members"
                        elif len(idx) == 1:
                            log.info("GFD: 1 member " + "S" + str(idx[0]))
                            message        = "1 member " + "S" + str(idx[0])+",1 Deleted"
                        elif len(idx) == 2:
                            log.info("GFD: 2 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) )
                            message        = "2 members " + "S" + str(idx[0]) + ", S" + str(idx[1])+",1 Deleted"
                        elif len(idx) == 3:
                            log.info("GFD: 3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2]))
                            message        = "3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2])+",1 Deleted"
                    # if self.thread_id == 0:

                    
                    s_rm.sendall(message.encode())
                    # print("sent",message)


                except:
                    time.sleep(10)
                    print("Lfd num " + str(self.lfd_num) + " is not responding.")
                    self.run()
                 

#main
sample = Sample(0,10000,port_num=port1)
sample.start()      # Initiates second thread which calls sample.run()
# sample.test()       # Main thread calls sample.test

sample1 = Sample(1,10001,port_num=port2)
sample1.start()
# sample1.test2()

sample2 = Sample(2,10002,port_num=port3)
sample2.start()
# sample2.test2()
