from __future__ import annotations

import socket
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
import subprocess
import sys
from pathlib import Path

from robot.ipc.config import Config
from robot.ipc.socket_json import send_json, recv_json
from robot.model.direction import Direction


class CannotFindPythonExecutable(Exception):
    pass


def _run_server() -> int:
    if not sys.executable:
        raise CannotFindPythonExecutable
    
    pythonw_path = Path(sys.executable).parent / "python"
    p = Popen([pythonw_path, "-m", "robot.ipc.server"],
          stdin=PIPE,
          stdout=PIPE,
          stderr=PIPE,
          shell=False,
          creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW,
          )

    return p.pid


class Proxy:

    def __init__(self, connect_attempts: int = 10) -> None:
        self._host = Config.HOST
        self._port = Config.PORT
        self._client = None
        self._server_pid = None
        self._attempts = connect_attempts

    def is_wall(self, direction: Direction) -> bool:
        command = {"command": "is_wall", "direction": str(direction)}
        response = self.send(command, need_answer=True)
        return response["result"]

    def step(self, direction: Direction) -> None:
        command = {"command": "step", "direction": str(direction)}
        self.send(command)

    def paint(self) -> None:
        command = {"command": "paint"}
        self.send(command)

    def end(self) -> None:
        command = {"command": "quit"}
        self.send(command)

    def load_field(self, file_name: str) -> None:
        command = {"command": "load", "field": file_name}
        self.send(command)

    def is_connected(self) -> bool:
        return self._client is not None

    def connect(self) -> None:
        if self.is_connected():
            return

        self._client = socket.socket()
        attempts = self._attempts
        while attempts:
            try:
                self._client.connect((self._host, self._port))
                if self._server_pid is not None:
                    print(f'Connected to server, pid: {self._server_pid}')
                    self.send({"command": "pid", "pid": self._server_pid})
                else:
                    print(f'Connected to server, pid unknown')
                break
            except ConnectionRefusedError:
                print('No server available, starting server...')
                attempts -= 1
                self._server_pid = _run_server()
        else:
            print(f"Couldn't connect to server (tried for {self._attempts} time{'s' if self._attempts > 1 else ''})")

    def send(self, data, need_answer: bool = False) -> dict | None:
        if not self.is_connected():
            raise ConnectionError('Unconnected to server')
        send_json(self._client, data)
        answer = recv_json(self._client)
        if need_answer:
            return answer

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __del__(self) -> None:
        self.close()
