from __future__ import annotations

import socket
from subprocess import Popen, PIPE
import sys

from .config import Config
from .socket_json import send_json, recv_json


def _run_server() -> None:
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    Popen([sys.executable, "server.py"],
          stdin=PIPE,
          stdout=PIPE,
          stderr=PIPE,
          creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
          )


class Sender:

    def __init__(self, attempts: int = 10) -> None:
        self._host = Config.HOST
        self._port = Config.PORT
        self._client = None
        self._attempts = attempts

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
                print('Connected to server')
                break
            except ConnectionRefusedError:
                print('No server available, starting server...')
                attempts -= 1
                _run_server()
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
