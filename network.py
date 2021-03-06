import socket
import pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.35"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()
        # print(self.player)

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2084*64))

