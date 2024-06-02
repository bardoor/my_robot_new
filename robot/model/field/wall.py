from robot.model.direction import Direction

class Wall:
    
    def __init__(self, direction: Direction) -> None:
        self._direction = direction

    def direction(self) -> Direction:
        return self._direction
     