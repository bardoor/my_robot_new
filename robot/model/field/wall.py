from ..direction import Direction


class Wall:
    def __init__(self, cell: 'Cell', direction: Direction):
        self._cell = cell
        self._direction = direction

    @property
    def direction(self):
        return self._direction
