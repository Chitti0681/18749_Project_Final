import threading
import time
import socket
import sys
from datetime import datetime

port1 = int(sys.argv[1])
port2 = int(sys.argv[2])
port3 = int(sys.argv[3])

GFD_MEMBERS   = [0, 0, 0]
GFD_MEM_COUNT = [0]
current_state = [1, 1, 1]

class Sample(threading.Thread):
    def __init__(self, thread_serv_type="lfd", port_num=10111):
        super(Sample, self).__init__()

        self.stop        = False
        self.type        = thread_serv_type
        self.port_num    = port_num
        self.port_num_rm = 10000

        self.lfd_num  = 0

    def run(self):
        if self.type == "lfd":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = self.port_num
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s.bind((localhost,port))
            print("Socket bound to %s" %(port))

            s.listen(5)
            print("Socket is listening")

            c,addr=s.accept()
            print("Got connnection from ", addr)

            # connect to the RM
            s_rm = socket.socket()
            print("Socket successfully created !!!")
            port = self.port_num_rm
            # localhost="127.0.0.1"
            localhost = "10.0.0.113"
            s_rm.bind((localhost,port))
            print("Socket bound to %s" %(port))

            s_rm.listen(5)
            print("Socket is listening")

            c_rm,addr_rm=s_rm.accept()
            print("Got connnection from ", addr_rm)


            while True:
                dateTimeObj  = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                try:
                    rcv_msg      = c.recv(1024)
                    # print("lfd has sent: ", rcv_msg.decode('utf-8'))
                    try:
                        a = int(rcv_msg.decode('utf-8')[-17]) 
                        if int(rcv_msg.decode('utf-8')[-17]) == int(rcv_msg.decode('utf-8')[-1]):
                            GFD_MEMBERS[int(rcv_msg.decode('utf-8')[-1]) - 1] = 1
                            self.lfd_num = int(rcv_msg.decode('utf-8')[-1])
                            GFD_MEM_COUNT[0] += 1
                            idx = []
                            n   = 0
                            for mem in GFD_MEMBERS:
                                if mem == 1:
                                    idx.append(n + 1)
                                n += 1
                            if len(idx) == 1:
                                print("GFD: 1 member " + "S" + str(idx[0]))
                                message        = "1 member " + "S" + str(idx[0])
                                s_rm.sendall(message.encode())
                            if len(idx) == 2:
                                print("GFD: 2 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) )
                                message        = "2 members " + "S" + str(idx[0]) + ", S" + str(idx[1])
                                s_rm.sendall(message.encode())
                            if len(idx) == 3:
                                print("GFD: 3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2]))
                                message        = "3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2])
                                s_rm.sendall(message.encode())
                    except:
                        # print("lfd has sent: ", rcv_msg.decode('utf-8'))
                        GFD_MEM_COUNT[0] -= 1
                        GFD_MEMBERS[int(rcv_msg.decode('utf-8')[-1]) - 1] = 0
                        idx = []
                        n   = 0
                        for mem in GFD_MEMBERS:
                            if mem == 1:
                                idx.append(n + 1)
                            n += 1
                        if len(idx) == 0:
                            print("GFD: 0 members")
                            message        = "0 members"
                            s_rm.sendall(message.encode())
                        if len(idx) == 1:
                            print("GFD: 1 member " + "S" + str(idx[0]))
                            message        = "1 member " + "S" + str(idx[0])
                            s_rm.sendall(message.encode())
                        if len(idx) == 2:
                            print("GFD: 2 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) )
                            message        = "2 members " + "S" + str(idx[0]) + ", S" + str(idx[1])
                            s_rm.sendall(message.encode())
                        if len(idx) == 3:
                            print("GFD: 3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2]))
                            message        = "3 members " + "S" + str(idx[0]) + ", S" + str(idx[1]) + ", S" + str(idx[2])
                            s_rm.sendall(message.encode())
                except:
                    time.sleep(10)
                    print("Lfd num " + str(self.lfd_num) + " is not responding.")
                    run()
                 

#main
sample = Sample(port_num=port1)
sample.start()      # Initiates second thread which calls sample.run()
# sample.test()       # Main thread calls sample.test

# sample1 = Sample(port_num=port2)
# sample1.start()
# # sample1.test2()

# sample2 = Sample(port_num=port3)
# sample2.start()
# sample2.test2()
