from __future__ import annotations

import socket
from subprocess import Popen, PIPE
import subprocess
import sys
from pathlib import Path
import os

from robot.ipc.config import Config
from robot.ipc.socket_json import send_json, recv_json
from robot.model.direction import Direction
from robot.model.robot.robot import StepResult


class CannotFindPythonError(Exception):
    pass


class CannotStartServerProcessError(Exception):

    def __init__(self, err_message: str, return_code: int) -> None:
        super().__init__(err_message)
        self.return_code = return_code


def _run_server() -> int:
    if not sys.executable:
        raise CannotFindPythonError
    
    # Вместо python должен запускаться именно pythonw, т.к. он не вызывает отображение консольного окна
    pythonw_path = Path(sys.executable).parent / "pythonw"
    p = Popen([pythonw_path, "-m", "robot.ipc.run_ui"],
              stdin=PIPE,
              stdout=PIPE,
              stderr=PIPE,
              shell=False,
              creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW,
              )
    
    # В случае, если процесс сервера успешно запустился, он будет крутится
    # до тех пор пока мы сами его не закроем. В случае ошибки, процесс перестанет выполнятся
    # и вернется код ошибки, а из stderr можно будет прочитать текст ошибки.
    # В коде ниже ждем 2 секунды для запуска, и надеемся, что если какие-то ошибки произойдут,
    # то случатся они именно за эти две секунды, мы их отловим, и выкинем свое исключение по этому поводу.
    # Если случилось исключение TimeoutExpired, значит процесс сервера запустился успешно.
    timeout = 2
    try:
        return_code = p.wait(timeout=timeout)
        err_message = p.stderr.read().decode()
        raise CannotStartServerProcessError(err_message=err_message, return_code=return_code)
    except subprocess.TimeoutExpired:
        pass


class UISuddenlyClosedError(RuntimeError):
    pass


class Proxy:

    def __init__(self) -> None:
        self._host = Config.HOST
        self._port = Config.PORT
        self._client = None

    def is_wall(self, direction: Direction) -> bool:
        request = {
            "command": "is_wall",
            "direction": str(direction),
            }
        response = self._communicate(request)
        return response["result"]

    def step(self, direction: Direction) -> StepResult:
        request = {
            "command": "step",
            "direction": str(direction),
            }
        response = self._communicate(request)
        if response["status"] == "crashed":
            return StepResult.HIT_WALL
        return StepResult.OK

    def paint(self) -> None:
        request = {
            "command": "paint",
            }
        self._communicate(request)

    def load_field(self, file_name: str) -> None:
        request = {
            "command": "load",
            "field": str(Path(file_name).resolve()),
            }
        self._communicate(request)

    def _send_initialize_request(self) -> None:
        pid = os.getpid()
        initalize_request = {"command": "register", "pid": pid}
        self._communicate(initalize_request)

    def is_connected(self) -> bool:
        return self._client is not None

    def connect(self, max_tries: int = 5) -> None:
        if self.is_connected():
            return

        self._client = socket.socket()

        tries = 0
        while True:
            if tries == max_tries:
                raise TimeoutError("Could not connect to server")

            try:
                self._client.connect((self._host, self._port))
                self._send_initialize_request()
                break
            except ConnectionRefusedError:
                _run_server()
                tries += 1

    def _communicate(self, data: dict) -> dict:
        if not self.is_connected(): self.connect()
        try:
            send_json(self._client, data)
            return recv_json(self._client)
        except ConnectionResetError:
            raise UISuddenlyClosedError('Графическое окно неожиданно закрылось') from None
        