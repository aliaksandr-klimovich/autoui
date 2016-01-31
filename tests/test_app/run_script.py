from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer, UDPServer
from threading import Thread


class CustomSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    # suppress stdout
    def log_message(self, format, *args):
        pass


class TestServer(object):
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    def start(self):
        self.server = UDPServer((self.host, self.port), CustomSimpleHTTPRequestHandler)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
