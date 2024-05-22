from __future__ import annotations

import socket
from subprocess import Popen, PIPE

from config import Config
from socket_json import send_json, recv_json


def _run_server() -> None:
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    Popen(["python", "server.py"],
          stdin=PIPE,
          stdout=PIPE,
          stderr=PIPE,
          creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
          )


class Connector:

    def __init__(self) -> None:
        self._host = Config.HOST
        self._port = Config.PORT
        self._client = None

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    def connect(self) -> None:
        self._client = socket.socket()
        tries = 10
        while tries:
            try:
                self._client.connect((self._host, self._port))
                print('Connected to server')
                break
            except ConnectionRefusedError:
                print('No server available, starting server...')
                tries -= 1
                _run_server()
        else:
            print("Couldn't connect to server")

    def send(self, data, need_answer: bool = False) -> dict | None:
        if not self.is_connected:
            raise ConnectionError('Unconnected to server')
        send_json(self._client, data)
        if need_answer:
            return recv_json(self._client)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __del__(self) -> None:
        self.close()


con = Connector()
con.connect()
print(con.send({'command': 'paint'}, need_answer=True))
con.send({'command': 'quit'})
