from __future__ import annotations
from typing import TYPE_CHECKING
import socket
import os
import sys
import signal

from robot.ipc.config import Config
from robot.ipc.parser import parse
from robot.ipc.socket_json import send_json, recv_json
from robot.ui.gui import GUI
from robot.ui import *
from robot.model.program import Program
from robot.model.robot.robot import StepResult
from robot.model.robot.robot_command import *


sys.stderr = open(os.path.dirname(os.path.realpath(__file__)) + '\\err.txt', 'w')


class Server:

    def __init__(self):
        self._program = Program()
        #self._program.add_listener(self)
        self._server = socket.socket()
        self._server.bind((Config.HOST, Config.PORT))
        self._server.listen(1)
        self._client = None
        self._client_addr = None
        self._gui = None
        self.__log_file = open(os.path.dirname(os.path.realpath(__file__)) + '\\log.txt', 'w')

    def has_client(self):
        return self._client is not None

    def accept(self):
        self._client, self._client_addr = self._server.accept()

    def run(self):
        self.accept()
        
        while True:
            print(1)
            command = recv_json(self._client)
            print(command)

            match command:
                case {'command': 'pid', "pid": pid}:
                    self._pid = pid
                    send_json(self._client, {"info": "saved pid"})
                case {'command': 'quit'}:
                    if self._gui is not None:
                        self._gui.kill()
                        self._gui.join()
                        send_json(self._client, {"info": "window closed"})
                        print(self._gui.is_alive())
                    break
                case {'command': 'load', 'field': file_name}:
                    self._program.load_field(file_name)
                    field_widget = FieldWidget(self._program.field())
                    main_window = MainWindow(BackingWidget(field_widget))
                    self._gui = GUI(main_window, self._pid)
                    self._program.start_execution(1.5)
                    send_json(self._client, {"info": "window opened"})
                case {'command': _}:
                    parsed_command = parse(command)
                    self._program.add_command(parsed_command)
                    result = self._program.get()
                    self.command_executed(parsed_command, result)
                case _:
                    raise ValueError
            
            print(3)

        self.close()
        os.kill(self._pid, signal.SIGTERM)
        print(555555555555555555)

    def command_executed(self, command: RobotCommand, result=None) -> None:
        robot_status = None
        command_type = None

        if isinstance(command, Step):
            command_type = "step"
            match result:
                case StepResult.OK:
                    robot_status = "alive"
                case StepResult.NOT_MOVED, StepResult.HIT_WALL:
                    robot_status = "crashed"
                case _:
                    raise ValueError
        elif isinstance(command, Paint):
            command_type = "paint"
            robot_status = "alive"
        elif isinstance(command, CheckWall):
            command_type = "is_wall"
            robot_status = "alive"
        else:
            raise ValueError

        response = {"robot": robot_status, "command_type": command_type}
        # Отвратительно...
        if isinstance(result, bool):
            response["result"] = result

        send_json(self._client, response)

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
