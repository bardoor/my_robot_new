import pytest
from model.direction import Direction
from model.program import Program
from model.robot.robot_command import CheckWall, Step, Paint


@pytest.fixture
def program():
    return Program()


@pytest.fixture
def commands():
    return zip(
        [CheckWall(Direction.SOUTH), CheckWall(Direction.NORTH), Step(Direction.NORTH), Paint(), Paint()],
        [True, False, True, True, True]
    )


def test_add_command(program, commands):
    for (command, _) in commands:
        program.add_command(command)


def test_exec_commands_sequential(program, commands):
    for (command, _) in commands:
        program.add_command(command)

    program.start_execution(0)

    for (_, res) in commands:
        assert program.get_results() is res
