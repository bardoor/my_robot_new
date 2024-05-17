import time, threading
from model.robot.robot_command import *


class Program:
    __commands: [RobotCommand]
    __current: int
    __timer: threading.Timer | None
    __results: [bool]

    def __init__(self):
        self.__commands = []
        self.__current = 0
        self.__timer = None
        self.__results = []

    def add_command(self, command: RobotCommand):
        self.__commands.append(command)

    def get_results(self):
        return self.__results

    def start_execution(self, interval: float):
        self.__timer = threading.Timer(interval, self.__execute_current)

    def __execute_current(self):
        if self.__current >= len(self.__commands):
            return None

        result = self.__commands[self.__current].execute()
        self.__results.append(result)
        self.__send_command_result(result)
        self.__current += 1

    def __send_command_result(self, result):
        pass

    def __end_execution(self):
        if self.__timer is None:
            return None
        self.__timer.cancel()




