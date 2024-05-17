from model.field.field import Field
from model.direction import Direction
import pytest
from model.field.exceptions import FieldSizeException


@pytest.fixture
def empty_field():
    field = Field("test_env_base.xml")
    return field


@pytest.fixture
def field_with_robot():
    field = Field("test_env_with_robot.xml")
    return field


def test_empty_field_creation(empty_field: Field):
    cells = list(empty_field.cells())
    assert len(cells) == 4

    assert cells[0].is_wall(Direction.WEST)
    assert cells[0].is_wall(Direction.NORTH)
    assert cells[0].is_wall(Direction.EAST)
    assert not cells[0].is_wall(Direction.SOUTH)
    assert cells[0].is_painted
    assert cells[0].robot is None

    assert cells[1].is_wall(Direction.NORTH)
    assert cells[1].is_wall(Direction.EAST)
    assert cells[1].is_wall(Direction.WEST)
    assert cells[1].is_wall(Direction.SOUTH)
    assert cells[1].is_painted
    assert cells[1].robot is None

    assert cells[2].is_wall(Direction.WEST)
    assert cells[2].is_wall(Direction.SOUTH)
    assert not cells[2].is_wall(Direction.EAST)
    assert not cells[2].is_wall(Direction.NORTH)
    assert cells[2].robot is None

    assert cells[3].is_wall(Direction.SOUTH)
    assert cells[3].is_wall(Direction.NORTH)
    assert not cells[3].is_wall(Direction.EAST)
    assert not cells[3].is_wall(Direction.WEST)
    assert not cells[3].is_painted
    assert cells[3].robot is None


def test_field_with_robot(field_with_robot: Field):
    cells = list(field_with_robot.cells())
    assert len(cells) == 4

    assert cells[0].is_wall(Direction.WEST)
    assert cells[0].is_wall(Direction.NORTH)
    assert not cells[0].is_wall(Direction.EAST)
    assert not cells[0].is_wall(Direction.SOUTH)
    assert cells[0].is_painted
    assert cells[0].robot is None

    assert cells[1].is_wall(Direction.NORTH)
    assert cells[1].is_wall(Direction.EAST)
    assert cells[1].is_wall(Direction.WEST)
    assert cells[1].is_wall(Direction.SOUTH)
    assert cells[1].is_painted
    assert cells[1].robot is None

    assert cells[2].is_wall(Direction.WEST)
    assert cells[2].is_wall(Direction.SOUTH)
    assert not cells[2].is_wall(Direction.EAST)
    assert not cells[2].is_wall(Direction.NORTH)
    assert cells[2].robot is not None

    assert cells[3].is_wall(Direction.SOUTH)
    assert not cells[3].is_wall(Direction.EAST)
    assert not cells[3].is_wall(Direction.NORTH)
    assert not cells[3].is_wall(Direction.WEST)
    assert not cells[3].is_painted
    assert cells[3].robot is None


def test_field_wrong_size():
    with pytest.raises(FieldSizeException):
        Field("test_env_wrong_size.xml")
