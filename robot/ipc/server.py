from __future__ import annotations
import socket
import os

from robot.ipc.config import Config
from robot.ipc.parser import parse
from robot.model.program import Program
from robot.ipc.socket_json import send_json, recv_json

from robot.ui.gui import GUI
from robot.ui import *


class Server:

    def __init__(self):
        self._program = Program()
        self._program.add_listener(self)
        self._server = socket.socket()
        self._server.bind((Config.HOST, Config.PORT))
        self._server.listen(1)
        self._client = None
        self._client_addr = None
        self._gui = None
        self.__log_file = open(os.path.dirname(os.path.abspath(__file__)) + '\log.txt', 'w')

    def has_client(self):
        return self._client is not None

    def accept(self):
        self._client, self._client_addr = self._server.accept()

    def run(self):
        self.accept()
        
        while True:
            command = recv_json(self._client)
            match command:
                case {'command': 'quit'}:
                    if self._gui is not None:
                        self._gui.kill()
                    break
                case {'command': 'load', 'field': file_name}:
                    self._program.load_field(file_name)
                    field_widget = FieldWidget(self._program.field())
                    main_window = MainWindow(BackingWidget(field_widget))
                    self._gui = GUI(main_window)
                    self._program.start_execution(3)
                case {'command': _}:
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


_server = Server()
_server.run()
