import threading
import time
import socket
import sys
from datetime import datetime
import logging

##### global current state ######
current_state = [0, 0, 0]


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger("my-logger")


class Sample(threading.Thread):
    def __init__(self, thread_serv_type, thread_id):
        super(Sample, self).__init__()

        self.stop = False
        self.type = thread_serv_type
        self.thread_id = thread_id
    '''
        Get the current timestamp
        @param none
        @return timestamp
    '''

    def get_current_timestamp(self):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return timestampStr

    '''
        Update the client state
        @param received message from client
        @return None
    '''

    def update_client_state(self, rcv_msg):

        log.info("The client id is : " + rcv_msg.decode('utf-8')[-13])
        log.info("My current state "+str(current_state) +
                 " before processing the request")
        current_state[int(rcv_msg.decode('utf-8')[-13]) -
                      1] = int(rcv_msg.decode('utf-8')[-2])
        log.info("My current state " + str(current_state) +
                 "  after processing request")

    '''
        Create a socket of the given port and ip address
        @param port, localhost
        @return socket object,connection object and ip address

    '''

    def create_socket(self, port, localhost):
        s = socket.socket()
        print("Socket successfully created !!!")
        s.bind((localhost, port))
        print("Socket bound to %s" % (port))

        s.listen(5)
        print("Socket is listening")

        c, addr = s.accept()
        print("Got connnection from ", addr)

        return c, addr, s

    '''
        The main run function
    '''

    def run(self):
        global become_primary
        global logs
        global rcv_checkpoint
        global rply_from_logs
        global server_type
        global CLIENT_PORT
        global PRIMARY_PORT_1
        global PRIMARY_PORT_2
        global checkpoint_count
        ######### Code for receiving message from RM ########

        if self.type == "RM":

            port = RM_PORT
            localhost = "10.0.0.189"

            ##### Create and listen on this socket ####
            c, addr, s = self.create_socket(port, localhost)

            while True:
                try:

                    rcv_msg = c.recv(1024)
                    ####### Decode the message from RM ######
                    server_type = int(rcv_msg.decode('utf-8')[0])
                    CLIENT_PORT = int(rcv_msg.decode('utf-8')[2:7])
                    PRIMARY_PORT_1 = int(rcv_msg.decode('utf-8')[8:13])
                    PRIMARY_PORT_2 = int(rcv_msg.decode('utf-8')[14:19])
                    # print("In RM")
                    if server_type == 0:
                        become_primary = 1
                        rply_from_logs = 1
                    # print("values",server_type,become_primary,rply_from_logs)
                    break
                except:
                    time.sleep(1)
                    s.listen(5)
                    c, addr = s.accept()

        ######### Code for serving client #########
        elif self.type == "client":

            port = CLIENT_PORT
            localhost = LOCALHOST

            ##### Create and listen on this socket ####
            c, addr, s = self.create_socket(port, localhost)

            while True:
                # print("Thread ID",self.thread_id)
                # print("Primary",become_primary)
                if self.thread_id == 0 and become_primary == 1:
                    print("exiting Thread")
                    break
                try:

                    ######## receive message and store in the logs #######
                    rcv_msg = c.recv(1024)
                    if rcv_msg.decode('utf-8') != "":
                        logs.append(rcv_msg)
                    # print("flag ",rply_from_logs)
                    # print("log ",logs)
                    ###### When replica becomes primary #########
                    if rply_from_logs == 1:
                        # print("inside the loop",logs)

                        ##### Indicate the client regarding the resend #####
                        if len(logs) != 0:
                            message = "resend"
                            c.send(message.encode())

                        ##### Reply to the messages in the logs #####
                        for i in range(0, len(logs)):
                            # print(i)
                            message_id = int(logs[i].decode('utf-8')[-7:-4])
                            #### Update the client state based on the received message #####
                            self.update_client_state(logs[i])

                            message = "<C" + str(logs[i].decode(
                                'utf-8')[-13]) + ", S, "+str(message_id)+", " + "state changed to " + str(logs[i].decode('utf-8')[-2]) + ">"
                            c.send(message.encode())
                            # print("sent")

                        ##### Indicate the client regarding the end of resend #####
                        if len(logs) != 0:
                            message = "end"
                            c.send(message.encode())

                        rply_from_logs = 0
                        # print("Done replying")
                    if rcv_checkpoint == 1:
                        logs = []
                        rcv_checkpoint = 0

                    ####### If the server is the primary #################
                    if server_type == 0:
                        message_id = int(rcv_msg.decode('utf-8')[-7:-4])
                        #### Update the client state based on the received message #####
                        self.update_client_state(rcv_msg)

                        message = "<C" + str(rcv_msg.decode(
                            'utf-8')[-13]) + ", S, "+str(message_id)+", " + "state changed to " + str(rcv_msg.decode('utf-8')[-2]) + ">"
                        c.send(message.encode())
                    if server_type == 1:
                        # time.sleep(1)
                        # print("Error")
                        s.listen(5)
                        c, addr = s.accept()
                except:
                    # print("Error")
                    s.listen(5)
                    c, addr = s.accept()

        #### Code for responding to LFD ######
        elif self.type == "lfd":

            port = LFD_PORT
            localhost = LOCALHOST

            ##### Create and listen on this socket ####
            c, addr, s = self.create_socket(port, localhost)

            while True:
                try:
                    rcv_msg = c.recv(1024)
                    log.info("From LDF: "+rcv_msg.decode('utf-8'))
                    message = ' Alive'
                    c.sendall(message.encode())
                    log.info('Server sent Alive')
                except:
                    log.info("The client has stopped responding")
                    time.sleep(2)
                    s.listen(5)
                    log.info("Socket is listening")
                    c, addr = s.accept()

        elif self.type == "replica":

            port = PRIMARY_PORT_1
            localhost = LOCALHOST

            ##### Create and listen on this socket ####
            s_replica, addr, s = self.create_socket(port, localhost)

            while True:
                try:
                    ###### When a replica receives checkpoint #####
                    rcv_msg = s_replica.recv(1024)
                    #message_id = int(rcv_msg.decode('utf-8')[-7:-4])
                    log.debug("Received "+rcv_msg.decode('utf-8'))

                    #### Update the client state based on the received message #####
                    # self.update_client_state(rcv_msg)

                    # timestampStr = self.get_current_timestamp()
                    current_state[0] = int(rcv_msg.decode('utf-8')[-9])
                    current_state[1] = int(rcv_msg.decode('utf-8')[-6])
                    current_state[2] = int(rcv_msg.decode('utf-8')[-3])

                    message = "<S_replica"+str(REPLICA_ID)+", S, state changed to " + \
                        str(rcv_msg.decode('utf-8')[-10:-1]) + ">"

                    s_replica.send(message.encode())
                    log.debug("Sent "+message)
                    ##### Set the flag to flush the log ######
                    rcv_checkpoint = 1
                except:
                    time.sleep(1)
                    s.listen(5)
                    s_replica, addr = s.accept()

                if become_primary == 1:
                    break

        elif self.type == "checkpoint":
            try:
                s_replica1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_replica2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print(
                    "Socket creation failed with error code %s" % (err))

            port_replica1 = PRIMARY_PORT_1
            port_replica2 = PRIMARY_PORT_2
            localhost_replica1 = LOCALHOST
            localhost_replica2 = LOCALHOST

            '''
            AF_INET-> refers to the address family IPv4
            SOCK_STREAM -> connection oriented TCP protocol

            '''
            try:
                s_replica1.connect((localhost_replica1, port_replica1))
                # print("The socket has successfull connected to the Server 1 on port == %s" % (
                #     localhost1))
            except:
                log.info("S1 replica Down")

            try:
                s_replica2.connect((localhost_replica2, port_replica2))
                # print("The socket has successfull connected to the Server 1 on port == %s" % (
                #     localhost1))
            except:
                log.info("S2 replica Down")

            current_checkpoint_state = current_state
            try:

                replica_id = 1
                message = "<S, S_replica" + \
                    str(replica_id) + ", " + str(checkpoint_count) + \
                    ", " + str(current_checkpoint_state) + ">"

                log.info("Sent "+message)
                rcv_checkpoint = 1
                s_replica1.send(message.encode())
                rcv_message1 = s_replica1.recv(1024)
                log.info("Received "+rcv_message1.decode('utf-8'))

            except:
                log.info("The Server Replica 1 is not responding")
                time.sleep(2)

            try:

                replica_id = 2
                message = "<S, S_replica" + \
                    str(replica_id) + ", " + str(checkpoint_count) + \
                    ", " + str(current_checkpoint_state) + ">"

                log.info("Sent "+message)

                s_replica2.send(message.encode())
                rcv_message2 = s_replica2.recv(1024)
                log.info("Received "+rcv_message2.decode('utf-8'))

            except:
                log.info("The Server Replica 2 is not responding")
                time.sleep(2)


# server_type = int(input("Enter the server type (p = 0 or r = 1): "))

# LFD_PORT = int(input("LFD port: "))  # 10113
# LOCALHOST = input("IP Address: ")  # "10.0.0.189"

server_type = int(sys.argv[1])

LFD_PORT = int(sys.argv[2])  # 10113
LOCALHOST = sys.argv[3]  # "10.0.0.189"

CLIENT_PORT = 0
PRIMARY_PORT_1 = 0
PRIMARY_PORT_2 = 0
become_primary = 0
logs = []
rcv_checkpoint = 0
rply_from_logs = 0
checkpoint_count = 0

# if server_type == 0:
#     PRIMARY_PORT_1 = int(input("Checkpoint port Replica 1: "))  # 10119
#     PRIMARY_PORT_2 = int(input("Checkpoint port Replica 2: "))  # 10120
# elif server_type == 1:
#     REPLICA_ID = int(input("Enter the Replica id: "))
#     PRIMARY_PORT = int(input("Checkpoint port Replica : "))

# CLIENT_PORT = int(input("Client port: "))  # 10116
# RM_PORT = int(input("Input the RM port: "))

REPLICA_ID = int(sys.argv[4])
PRIMARY_PORT_1 = int(sys.argv[5])  # 10119
PRIMARY_PORT_2 = int(sys.argv[6])  # 10120
CLIENT_PORT = int(sys.argv[7])  # 10116
RM_PORT = int(sys.argv[8])
##### Start thread to listen to RM ######
RM = Sample("RM", 10)
RM.start()

######## Start thread to listen to LFD  ########
sample3 = Sample("lfd", 3)
sample3.start()

####### Start the client ######
sample = Sample("client", 0)
sample.start()

####### Start the primary ######
if server_type == 0:
    print("Hi")
    while (True):
        checkpoint_count += 1
        time.sleep(15)
        sample6 = Sample("checkpoint", 6)
        sample6.start()
        sample6.join()

######## Start the LFD ########
elif server_type == 1:
    sample4 = Sample("replica", 4)
    sample4.start()


######## Check for messages from the RM ######
while True:
    if become_primary == 1:
        # print("in")
        #### end the replica thread ####
        # sample4.join()
        # sample.join()
        sample5 = Sample("client", 5)
        sample5.start()
        log.info("Now Primary")
        while (True):
            if rply_from_logs == 0:
                checkpoint_count += 1
                sample2 = Sample("checkpoint", 2)
                sample2.start()
                sample2.join()
                time.sleep(15)

        break
