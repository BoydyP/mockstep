import socket

class TelnetConnection:
    def __init__(self, host, port, timeout=10):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)

    def read_until(self, expected, timeout=10):
        self.sock.settimeout(timeout)
        data = b""
        while expected not in data:
            data += self.sock.recv(4096)
        return data

    def write(self, data):
        self.sock.sendall(data)

    def close(self):
        self.sock.close()
