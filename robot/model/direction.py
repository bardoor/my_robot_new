from enum import Enum


class Direction(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'
    EAST = 'east'

    @staticmethod
    def opposite(direction: 'Direction'):
        match direction:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST

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
