import time, threading
import queue

from robot.model.field.field import Field
from robot.model.robot.robot_command import *
from robot.ipc.timer import PyTimer


class Program:

    def __init__(self, robot) -> None:
        self._results = queue.Queue()
        self._commands = queue.Queue()
        self._timer = PyTimer(interval=None, timer_handler=self._execute_current)
        self._robot = robot

    def add_command(self, command: RobotCommand) -> None:
        command.set_robot(self._robot)
        self._commands.put(command)

    def start_execution(self, interval: float) -> None:
        self._timer.interval = interval
        self._timer.start()

    def get_result(self):
        return self._results.get()

    def _execute_current(self) -> None: 
        command = self._commands.get()
        result = command.execute()
        self._results.put(result)

    def end_execution(self) -> None:
        if self._timer is None:
            return
        self._timer.stop()
