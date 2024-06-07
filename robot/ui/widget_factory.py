from __future__ import annotations
from typing import Any, TYPE_CHECKING
from functools import singledispatchmethod

from robot.ui.cell_widget import CellWidget
from robot.ui.robot_widget import RobotWidget
from robot.ui.wall_widget import WallWidget
from robot.ui.core import Widget
from robot.model.field import Cell, Wall
from robot.model.robot import Robot

if TYPE_CHECKING:
    from robot.model.direction import Direction


class WidgetFactory:
    
    def __init__(self) -> None:
        self._cells = {}
        self._robot = {}
        self._walls = {}

    def create_blank_wall(self, cell: Cell, direction: Direction) -> WallWidget:
        return WallWidget(cell, direction)

    @singledispatchmethod
    def create(self, obj: Any) -> Widget:
        raise NotImplementedError()
    
    @create.register
    def _(self, obj: Cell) -> CellWidget:
        if obj in self._cells:
            return self._cells[obj]
        
        cell_widget = CellWidget(obj)
        if obj.has_robot():
            robot_widget = self.create(obj.robot())
            cell_widget.add_item_widget(robot_widget)

        self._cells[obj] = cell_widget
        return cell_widget

    @create.register
    def _(self, obj: Robot) -> RobotWidget:
        if obj in self._robot:
            return self._robot[obj]
        
        robot_widget = RobotWidget(obj)
        self._robot[obj] = robot_widget
        return robot_widget
    
    @create.register
    def _(self, obj: Wall) -> WallWidget:
        if obj in self._walls:
            return self._walls[obj]
        
        wall_widget = WallWidget(obj.cell(), obj.direction(), obj)
        self._walls[obj] = wall_widget
        return wall_widget

