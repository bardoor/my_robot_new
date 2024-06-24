from __future__ import annotations
import json
from pathlib import Path

from robot.model.field import Field
from robot.model.robot import Robot
from robot.model.field import Wall
from robot.model.direction import Direction
from robot.serialize.base import (
    NotFieldFileError,
    FieldFileNotFoundError,
    add_extension_if_not_present,
    file_exists,
    get_ext,
    )


class FieldReader:
    """
    Класс для чтения json файлов, которые содержат в себе обстановку поля
    А также для заселения поля по прочитанной обстановки
    """
    def __init__(self, field_config: dict) -> None:
        self._height = field_config["height"]
        self._width = field_config["width"]
        self._robot = field_config.get("robot", None)
        self._painted = field_config.get("painted", [])
        self._walls = field_config.get("walls", [])

    def _load(self, file_name: str | Path) -> None:
        if isinstance(file_name, str) and not file_name.endswith(".json"):
            file_name = f"{file_name}.json"

        path = Path(file_name)
        if not path.exists() or not path.is_file() or path.suffix != ".json":
            raise ValueError(".json file was expected as an environment file")
        
        with open(path, "r") as file:
            env_config = json.load(file)
            self._height = env_config["height"]
            self._width = env_config["width"]
            self._robot = env_config.get("robot", None)
            self._painted = env_config.get("painted", [])
            self._walls = env_config.get("walls", [])

    def _populate(self, field: Field) -> None:
        for painted_cell_pos in self._painted:
            field.get_cell(painted_cell_pos["x"], painted_cell_pos["y"]).paint()

        if self._robot is not None:
            x, y = self._robot["x"], self._robot["y"]
            field.get_cell(x, y).set_robot(Robot())

        if self._walls:
            for wall_info in self._walls:
                x, y, direction = wall_info["x"], wall_info["y"], Direction.from_str(wall_info["direction"])

                cell = field.get_cell(x, y)
                if cell.has_wall(direction):
                    continue
                
                cell.set_wall(direction, Wall(direction, cell))

    def load_field(self) -> Field:
        field = Field(self._width, self._height)
        self._populate(field)
        return field
    

def load_field_from_dict(field_config: dict) -> Field:
    '''Загружает поле из конфигурационного словаря'''
    return FieldReader(field_config).load_field()


def load_field_from_json(file_name: str | Path) -> None:
    '''Загружает поле из конфигурационного json файла'''
    if not file_exists(file_name):
        raise FieldFileNotFoundError
    
    ext = get_ext(file_name)
    if ext and ext != 'json':
        raise NotFieldFileError("Expected file with .json extension or no extension at all")

    file_name = add_extension_if_not_present(file_name, 'json')
    with open(file_name, "r") as file:
        field_config = json.load(file)
    return load_field_from_dict(field_config)
