from .cell import Cell
from ..robot.robot import Robot
from ..direction import Direction
import xml.etree.ElementTree as et
from .exceptions import *


# TODO сделать класс seeder, который будет брать обстановку в файле (или ещё где-то)
# и заполнять поле, а оно автоматически будет ставить ссылки на соседей
# возможно методы типа add_in_row(), add_in_col()
class Field:

    def __init__(self, height: int, width: int) -> None:
        self._validate(height, width)
        self._height = height
        self._width = width

        self._cells = []
        self._cells_map = {}
        self._generate_field()

    def _validate(self, height: int, width: int) -> None:
        if not isinstance(height, int) or not isinstance(width, int):
            raise TypeError('"height" and "width" both must be int type')
        if height <= 0 or width <= 0:
            raise ValueError('"height" and "width" both must be positive numbers')

    def width(self) -> int:
        return self._width
    
    def height(self) -> int:
        return self._height

    def cells(self):
        return self._cells

    def add_row(self) -> None:
        pass

    def add_col(self) -> None:
        pass

    def _generate_field(self):
        start_cell = Cell()
        self._cells_map['left_top'] = start_cell
        self._cells_map['right_top'] = start_cell
        self._cells_map['left_bottom'] = start_cell
        self._cells_map['right_bottom'] = start_cell

        self._cells.append(start_cell)

        current_row = start_cell
        for i in range(self._height):
            current_col = current_row
            self._cells_map['left_bottom'] = current_col

            for j in range(1, self._width):
                next_cell = Cell()
                self._cells.append(next_cell)
                current_col.set_neighbor(Direction.EAST, next_cell)
                current_col = next_cell
                self._cells_map['right_bottom'] = current_col

            if i + 1 < self._height:
                next_row = Cell()
                self._cells.append(next_row)
                current_row.set_neighbor(Direction.SOUTH, next_row)
                current_row = next_row

    def _generate(self):
        root = et.parse(environment_path).getroot()
        rows = root.findall("row")

        self._height = len(rows)
        self._width = len(rows[0])

        # TODO проверка корректности расстановки стен
        # TODO Вынести это всё в сущность парсер, чтоб поле не знало о файлике с обстановкой

        for row in rows:
            if len(row) != self._width:
                raise RowSizeException(self._width, len(row))

            cells = row.findall("cell")
            for cell in cells:
                cell_walls = []

                if (walls := cell.get("walls", None)) is not None:
                    walls = walls.split(" ")
                    for direction in walls:
                        cell_walls.append(Direction.from_str(direction))

                cell_is_painted = cell.get("painted") == "True"
                robot = Robot() if cell.get("robot") == "True" else None
                self._cells.append(Cell(cell_is_painted, cell_walls, robot))

        self._set_neighbors()

    def _set_neighbors(self):
        cells_matrix = self._as_matrix()
        for row in range(0, self._height):
            for col in range(0, self._width):
                if row > 0:
                    cells_matrix[row][col].set_neighbor(Direction.NORTH, cells_matrix[row - 1][col])
                if row < self._height - 1:
                    cells_matrix[row][col].set_neighbor(Direction.SOUTH, cells_matrix[row + 1][col])
                if col > 0:
                    cells_matrix[row][col].set_neighbor(Direction.WEST, cells_matrix[row][col - 1])
                if col < self._width - 1:
                    cells_matrix[row][col].set_neighbor(Direction.EAST, cells_matrix[row][col + 1])

    def _as_matrix(self):
        matrix = []

        for i in range(0, len(self._cells), self._width):
            row = self._cells[i: i + self._width]
            matrix.append(row)

        return matrix

    def robot(self):
        for cell in self._cells:
            if cell.robot is not None:
                return cell.robot
