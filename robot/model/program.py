import time, threading

from robot.model.field.field import Field
from robot.model.robot.robot_command import *
from robot.model.field import load_field


class Program:

    def __init__(self) -> None:
        self._commands = []
        self._current = 0
        self._timer = None
        self._execution_listeners = []
        self._field = None

    def load_field(self, file_name: str) -> None:
        self._field = load_field(file_name)

    def field(self) -> Field | None:
        return self._field

    def add_command(self, command: RobotCommand) -> None:
        command.set_robot(self._field.robot)
        self._commands.append(command)

    def start_execution(self, interval: float) -> None:
        self._timer = threading.Timer(interval, self.__execute_current)
        self._timer.start()

    def _execute_current(self) -> None: 
        if self._current >= len(self._commands):
            return

        result = self._commands[self._current].execute()
        self.fire_command_executed(result)
        self._current += 1

    def end_execution(self) -> None:
        if self.__timer is None:
            return
        self._timer.cancel()

    def add_listener(self, listener) -> None:
        self._execution_listeners.append(listener)

    def fire_command_executed(self, result) -> None:
        for listener in self._execution_listeners:
            listener.command_executed(result)
