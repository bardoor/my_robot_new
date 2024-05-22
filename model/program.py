import time, threading

from model.field.field import Field
from model.robot.robot_command import *


class Program:
    def __init__(self):
        self.__commands = []
        self.__current = 0
        self.__timer = None
        self.__results = []
        self.__execution_listeners = []
        self.__log_file = open('loh.txt', 'w')
        self.__field = None

    def add_command(self, command: RobotCommand):
        command.set_robot(self.__field.robot)
        self.__commands.append(command)

    def get_results(self):
        return self.__results

    def start_execution(self, interval: float):
        self.__field = Field("../sample_environment.xml")
        self.__timer = threading.Timer(interval, self.__execute_current)

    def __execute_current(self):
        print(1, file=self.__log_file)

        if self.__current >= len(self.__commands):
            return None

        result = self.__commands[self.__current].execute()
        print(str(result), file=self.__log_file)
        self.fire_command_executed(result)
        self.__current += 1

    def __end_execution(self):
        if self.__timer is None:
            return None
        self.__timer.cancel()

    def add_listener(self, listener):
        self.__execution_listeners.append(listener)

    def fire_command_executed(self, result):
        for listener in self.__execution_listeners:
            listener.commandExecuted(result)
