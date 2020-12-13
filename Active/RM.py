import threading
import time
import socket
import sys
from datetime import datetime

port1 = int(sys.argv[1])
# port2 = int(sys.argv[2])
# port3 = int(sys.argv[3])

RM_MEMBERS   = [0, 0, 0]
RM_MEM_COUNT = [0]
current_state = [1, 1, 1]

class Sample(threading.Thread):
    def __init__(self, thread_serv_type="gfd", port_num=10111):
        super(Sample, self).__init__()

        self.stop     = False
        self.type     = thread_serv_type
        self.port_num = port_num

        self.gfd_num  = 0

    def run(self):
        if self.type == "gfd":
            s=socket.socket()
            print("Socket successfully created !!!")
            port = self.port_num
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
                try:
                    rcv_msg      = c.recv(1024)
                    # print("lfd has sent: ", rcv_msg.decode('utf-8'))
                    try:
                        a = rcv_msg.decode('utf-8')
                        print("RM: " + str(a))

                except:
                    time.sleep(10)
                    print("GFD" + " is not responding.")
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
# # sample2.test2()
