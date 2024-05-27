from __future__ import annotations
from enum import Enum


class Direction(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'
    EAST = 'east'

    def opposite(self) -> Direction:
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST

    def clockwise(self) -> Direction:
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

    def anticlockwise(self) -> Direction:
        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.NORTH

    @staticmethod
    def from_str(direction: str):
        match direction.lower():
            case "north":
                return Direction.NORTH
            case "south":
                return Direction.SOUTH
            case "east":
                return Direction.EAST
            case "west":
                return Direction.WEST

    def __str__(self) -> str:
        return self.value
