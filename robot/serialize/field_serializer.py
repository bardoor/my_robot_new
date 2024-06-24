import json

from robot.model.field import Field
from robot.serialize.base import (
    NotFieldFileError,
    add_extension_if_not_present,
    get_ext,
    )


class FieldSerializer:
    """
    Класс для сериализации поля, выгрузки его в формат json
    """
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
                if self._field.get_cell(x, y).robot() is not None:
                    return {'x': x, 'y': y}
        return None
    
    def dump_field(self) -> None:
        env_config = {'height': self._field.height(), 'width': self._field.width()}
        walls = self._get_walls()
        env_config['walls'] = walls

        painted = self._get_painted_pos()
        env_config['painted'] = painted

        robot = self._get_robot_pos()
        env_config['robot'] = robot

        return env_config


def dump_field_as_dict(field: Field) -> dict:
    '''Сериализует поле в виде словаря'''
    return FieldSerializer(field).dump_field()


def dump_field_to_json(field: Field, file_name: str) -> None:
    '''Сериализует поле в виде json файла'''
    field_config = dump_field_as_dict(field)

    ext = get_ext(file_name)
    if ext and ext != 'json':
        raise NotFieldFileError("Expected file with .json extension or no extension at all")

    file_name = add_extension_if_not_present(file_name, 'json')
    with open(file_name, 'w') as config_file:
        json.dump(field_config, config_file, indent=4)
