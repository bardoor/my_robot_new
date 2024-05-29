import json
from pathlib import Path

from robot.model.field import Field


class FieldReader:
    
    def __init__(self, env_file: str) -> None:
        self._load(env_file)

    def _load(self, env_file: str) -> None:
        path = Path(env_file)
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

        # TODO: установка стен, установка робота...

    def get_field(self) -> Field:
        field = Field(self._width, self._height)
        self._populate(field)
        return field
    

def load_field(env_file: str | Path) -> Field:
    return FieldReader(env_file).get_field() 