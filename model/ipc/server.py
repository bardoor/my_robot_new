from __future__ import annotations
import socket

from model.ipc.config import Config
from model.ipc.parser import parse
from model.program import Program
from socket_json import send_json, recv_json


class Server:

    def __init__(self):
        self._program = Program()
        self._program.add_listener(self)
        self._server = socket.socket()
        self._server.bind((Config.HOST, Config.PORT))
        self._server.listen(1)
        self._client = None
        self._client_addr = None
        self.__log_file = open('loh.txt', 'w')

    def has_client(self):
        return self._client is not None

    def accept(self):
        self._client, self._client_addr = self._server.accept()

    def run(self):
        self.accept()
        self._program.start_execution(3)

        while True:
            command = recv_json(self._client)
            if 'command' in command and 'quit' == command['command']:
                break
            self._program.add_command(parse(command))

        self.close()

    def command_executed(self, result):
        print(str(result), file=self.__log_file)
        send_json(self._client, {"status": result})

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = self._client_addr = None
        if self._server is not None:
            self._server.close()
            self._server = None

    def __del__(self):
        self.close()
        self._server = None


server = Server()
server.run()
