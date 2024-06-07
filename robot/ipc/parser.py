from robot.model.robot.robot_command import (
    RobotCommand,
    Step,
    Paint,
    CheckWall,
)
from robot.model.direction import Direction
from robot.model.robot.robot import StepResult


def parse(json_data) -> RobotCommand:
    if 'command' not in json_data:
        raise ValueError("Expected a command to parse")
    match json_data['command']:
        case 'step':
            return Step(Direction.from_str(json_data['direction']))
        case 'paint':
            return Paint()
        case 'is_wall':
            return CheckWall(Direction.from_str(json_data['direction']))
        case unsupported:
            raise RuntimeError(f'Unsupported command: {unsupported}')
        

def unparse(data) -> dict:
    pass