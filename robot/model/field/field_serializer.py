from pathlib import Path
import json

from robot.model.field import Field


class FieldSerializer:
    
    def __init__(self, field: Field) -> None:
        self._field = field

    def _get_walls(self) -> list[tuple[int, int]]:
        seen_walls = []
        walls_info = []
        
        for x in range(self._field.width()):
            for y in range(self._field.height()):
                cell = self._field.get_cell(x, y)

                for direction, wall in cell.walls().items():
                    if wall not in seen_walls:
                        seen_walls.append(wall)
                        walls_info.append({"x": x, "y": y, "direction": str(direction)})

        return walls_info

    def _get_painted_pos(self) -> list[tuple[int, int]]:
        painted = []
        for x in range(self._field.width()):
            for y in range(self._field.height()):
                if self._field.get_cell(x, y).is_painted():
                    painted.append({'x': x, 'y': y})
        return painted

    def _get_robot_pos(self) -> tuple[int, int] | None:
        for x in range(self._field.width()):
            for y in range(self._field.height()):
                if self._field.get_cell(x, y).get_robot() is not None:
                    return {'x': x, 'y': y}
        return None
    
    def dump_field(self, file_name: str | Path) -> None:
        env_config = {'height': self._field.height(), 'width': self._field.width()}
        walls = self._get_walls()
        env_config['walls'] = walls

        painted = self._get_painted_pos()
        env_config['painted'] = painted

        robot = self._get_robot_pos()
        env_config['robot'] = robot

        with open(file_name, 'w') as output:
            json.dump(env_config, output)


def dump_field(field: Field, file_name: str) -> None:
    FieldSerializer(field).dump_field(file_name)