from ..direction import Direction


class Cell:

    def __init__(self, is_painted: bool = False, walls: list[Direction] = None, robot: 'Robot' = None):
        self._is_painted = is_painted
        self._walls = self._generate_walls(walls)
        self._neighbors = {}
        self._robot = robot
        if self._robot is not None:
            self._robot.cell = self

    def walls(self):
        return iter(self._walls)

    @property
    def robot(self):
        return self._robot

    @robot.setter
    def robot(self, new_robot):
        if new_robot is None and self._robot is not None:
            old_robot = self._robot
            self._robot = None
            old_robot.cell = None
            return

        self._robot = new_robot

        if (self._robot is not None) and (self is not new_robot.cell):
            new_robot.cell = self

    @property
    def is_painted(self) -> bool:
        return self._is_painted

    def paint(self) -> None:
        self._is_painted = True

    def is_wall(self, direction: Direction):
        return direction in self._walls

    def set_neighbor(self, direction: Direction, cell: 'Cell'):
        self._neighbors[direction] = cell
        if cell.get_neighbor(Direction.opposite(direction)) is None:
            cell.set_neighbor(Direction.opposite(direction), self)

    def get_neighbor(self, direction: Direction):
        if direction in self._neighbors:
            return self._neighbors[direction]
        return None

    def _generate_walls(self, walls_directions: list[Direction]):
        walls = []
        for wall_dir in walls_directions:
            walls.append(Wall(self, wall_dir))
        return walls
