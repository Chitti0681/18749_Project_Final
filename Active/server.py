import socket
from datetime import datetime
import time

current_state = [0, 0, 0]
s=socket.socket()

print("Socket successfully created !!!")

port = 10106
localhost="127.0.0.1"
s.bind((localhost,port))
print("Socket binded to %s" %(port))

s.listen(5)
print("Socket is listening")

c,addr=s.accept()
print("Got connnection from ", addr)
while True:
    
    try:
        dateTimeObj  = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        rcv_msg      = c.recv(1024)
        print("change state to ",  rcv_msg.decode('utf-8')[-2])
        print("The client id is : ", rcv_msg.decode('utf-8')[-13])

        current_state[int(rcv_msg.decode('utf-8')[-13]) - 1] = int(rcv_msg.decode('utf-8')[-2])
        print("the current state is ", current_state)

        # print("From LDF: ",rcv_msg.decode('utf-8'))
        message=timestampStr+' Alive'
        c.sendall(message.encode())
        print(timestampStr+'Server sent Alive')
    except:
        print("The LFD has stopped responding")
        time.sleep(2)
        s.listen(5)
        print("Socket is listening")
        c,addr=s.accept()

    
