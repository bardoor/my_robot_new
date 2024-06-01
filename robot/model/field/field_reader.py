import json
from pathlib import Path

from robot.model.field import Field
from robot.model.robot import Robot
from robot.model.field import Wall
from robot.model.direction import Direction


class FieldReader:
    
    def __init__(self, file_name: str) -> None:
        self._load(file_name)

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

                if field.get_cell(x, y).has_wall(direction):
                    continue
                
                field.get_cell(x, y).set_wall(direction, Wall())

    def get_field(self) -> Field:
        field = Field(self._width, self._height)
        self._populate(field)
        return field
    

def load_field(env_file: str | Path) -> Field:
    return FieldReader(env_file).get_field() 