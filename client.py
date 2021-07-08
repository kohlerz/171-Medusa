import socket
import threading
from joystick import Joystick

class Client:
    def __init__(self, xbox):
        HOST = '127.0.0.1'
        PORT = 6969

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.xbox = xbox
        self.connected = False
        self.failed_connections = 0

    def connect(self):
        try:
            self.sock.connect((self.HOST, self.PORT))
            self.connected = True
        except:
            if self.failed_connections >= 60:
                print("Failed to connect to Medusa")
                self.failed_connections = 0
            else:
                self.failed_connections += 1
            self.connected = False

    def send_data(self, data):
        if self.connected:
            try:
                self.sock.sendall(data.encode('ascii'))
            except:
                print("Failed to send data :(")
                self.connected = False

    def close(self):
        self.sock.close()
