import pytest

from model.direction import Direction
from model.field.field import Field


@pytest.fixture
def robot():
    return Field("environments/test_env_with_robot.xml").robot


def test_robot_step(robot):
    direction = Direction.NORTH
    start_cell = robot.cell
    end_cell = robot.cell.get_neighbor(direction)

    assert start_cell.robot == robot
    assert end_cell is not None
    assert end_cell.robot is None

    assert robot.step(direction) is True

    assert start_cell.robot is None
    assert end_cell.robot == robot


def test_robot_crashes(robot):
    direction = Direction.SOUTH
    start_cell = robot.cell
    end_cell = robot.cell.get_neighbor(direction)

    assert start_cell.robot == robot
    assert end_cell is None

    assert robot.step(direction) is False

    assert robot.cell == start_cell
    assert start_cell.robot == robot


def test_robot_paint_clean_cell(robot):
    assert robot.cell.is_painted is False
    assert robot.cell.paints_count == 0

    assert robot.paint() is True

    assert robot.cell.is_painted is True
    assert robot.cell.paints_count == 1


def test_robot_paint_painted_cell_once(robot):
    robot.step(Direction.NORTH)
    assert robot.cell.is_painted is True
    assert robot.cell.paints_count == 1

    assert robot.paint() is True

    assert robot.cell.is_painted is True
    assert robot.cell.paints_count == 2


def test_robot_paint_painted_cell_many_times(robot):
    robot.step(Direction.NORTH)
    assert robot.cell.is_painted is True
    assert robot.cell.paints_count == 1

    for _ in range(10):
        assert robot.paint() is True

    assert robot.cell.is_painted is True
    assert robot.cell.paints_count == 11


def test_robot_check_wall(robot):
    assert robot.is_wall(Direction.SOUTH)
    assert robot.is_wall(Direction.WEST)
    assert not robot.is_wall(Direction.EAST)
    assert not robot.is_wall(Direction.NORTH)

    assert robot.step(Direction.NORTH) is True

    assert robot.is_wall(Direction.NORTH)
    assert robot.is_wall(Direction.WEST)
    assert not robot.is_wall(Direction.SOUTH)
    assert not robot.is_wall(Direction.EAST)


