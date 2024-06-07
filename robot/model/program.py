import time, threading
import queue

from robot.model.field.field import Field
from robot.model.robot.robot_command import *
from robot.model.field import load_field
from robot.ipc._pytimer import PyTimer


class Program:

    def __init__(self) -> None:
        self._results = queue.Queue()
        self._commands = queue.Queue()
        self._current = 0
        self._timer = None
        self._execution_listeners = []
        self._field = None

    def load_field(self, file_name: str) -> None:
        self._field = load_field(file_name)

    def field(self) -> Field | None:
        return self._field

    def add_command(self, command: RobotCommand) -> None:
        command.set_robot(self._field.robot())
        self._commands.put(command)

    def start_execution(self, interval: float) -> None:
        self._timer = PyTimer(interval=interval, timer_handler=self._execute_current)
        self._timer.start()

    def get(self):
        return self._results.get()

    def _execute_current(self) -> None: 
        command = self._commands.get()
        result = command.execute()
        self._results.put(result)

    def end_execution(self) -> None:
        if self.__timer is None:
            return
        self._timer.stop()

    def add_listener(self, listener) -> None:
        self._execution_listeners.append(listener)

    def fire_command_executed(self, command, result) -> None:
        for listener in self._execution_listeners:
            listener.command_executed(command, result)
