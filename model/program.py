from robot.robot_command import *


class Program:
    __commands: [RobotCommand]

    def __init__(self):
        self.__commands = []

    def add_command(self, command: RobotCommand):
        self.__commands.append(command)

    def start_execution(self, speed: float):
        pass

    def __end_execution(self):
        pass



