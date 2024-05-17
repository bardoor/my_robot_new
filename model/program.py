import time, threading
from robot.robot_command import *


class Program:
    __commands: [RobotCommand]
    __current: int
    __timer: threading.Timer | None

    def __init__(self):
        self.__commands = []
        self.__current = 0
        self.__timer = None

    def add_command(self, command: RobotCommand):
        self.__commands.append(command)

    def start_execution(self, speed: float):
        self.__timer = threading.Timer(speed, self.__execute_current)

    def __execute_current(self):
        if self.__current >= len(self.__commands):
            return None

        self.__send_command_result(self.__commands[self.__current].execute())
        self.__current += 1

    def __send_command_result(self, result):
        pass

    def __end_execution(self):
        if self.__timer is None:
            return None
        self.__timer.cancel()




