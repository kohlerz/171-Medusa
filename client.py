import socket
import threading
import time
from joystick import Joystick

class Client:
    def __init__(self):
        self.HOST = '192.168.4.1'
        self.PORT = 6969

        # self.xbox = xbox
        self.connected = False
        self.failed_connections = 0
        self.send_time = 1
        self.messages = 0

        self.data = 'D 0.00 0.00'

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()


    def run(self):
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.settimeout(1.0)
        while True:
            try:
                if not self.connected:
                    s.settimeout(1.0)
                    s.connect((self.HOST, self.PORT))
                    # s.settimeout(None)
                    self.connected = True

                messages = 0
                while self.connected:
                    # s.sendall(self.data.encode('ascii'))
                    # time.sleep(self.send_time)
                 
                    if messages < 10:
                        self.send_data(s, self.data)
                        messages += 1
                    else:
                        self.send_data(s, "keepalive")
                        received = s.recv(16)
                        print(received)
                        messages = 0

            except:
                self.connected = False
                while not self.connected:
                    print("Couldn't connect, trying again")
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1.0)
                        s.connect((self.HOST, self.PORT))
                        self.connected = True
                    except:
                        self.connected = False
                    time.sleep(1)
                # s.settimeout(None)
                self.connected = True

    def send_data(self, s, data):
        if len(data) <= 11:
            for i in range(0, 11-len(data)):
                data += " "
            data += '\n'
            buffer = data.encode('ascii')
            # print(buffer)
            while buffer:
                bytes = s.send(buffer)
                buffer = buffer[bytes:]
            time.sleep(self.send_time)
        else:
            print("Data not formatted correctly")

    def close(self):
        self.connected = False