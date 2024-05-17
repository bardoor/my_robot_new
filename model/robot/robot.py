class Robot():
    _cell: Cell

    def __init__(self, cell: Cell | None = None) -> None:
        self._cell = cell

        if cell is not None:
            cell.robot = self

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, new_cell) -> None:
        if new_cell is None and self._cell is not None:
            old_cell = self._cell
            self._cell = None
            old_cell.robot = None
            return

        self._cell = new_cell

        if (self._cell is not None) and (self is not new_cell.robot):
            new_cell.robot = self

    def step(self, direction: Direction) -> bool:
        if self._cell.is_wall(direction):
            return False

        neighbor = self._cell.get_neighbor(direction)
        if neighbor is None:
            return False

        self._cell.robot = None
        neighbor.robot = self
        self._cell = neighbor
        return True

    def paint(self) -> bool:
        if self._cell.is_painted:
            return False

        self._cell.paint()
        return True

