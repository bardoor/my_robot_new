from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.model.direction import Direction
from robot.ui.core import Widget
from robot.ui.cell_widget import CellWidget
from robot.ui.wall_widget import WallWidget
from robot.ui.widget_factory import WidgetFactory


if TYPE_CHECKING:
    from robot.model.field import Field, Cell
    from robot.model.robot import Robot


class FieldWidget(Widget, RobotListener):
    # Зазор между клетками.
    # TODO: должна быть ширина (высота?) стены
    GAP = 10

    def __init__(self, field: Field) -> None:
        self._field = field
        self._widget_factory = WidgetFactory()
        
        if self._field.robot() is not None:
            self._field.robot().add_listener(self)

    def _make_field_surface(self):
        pixel_height = (
            self._field.height() * CellWidget.CELL_SIZE
            + (self._field.height() - 1) * WallWidget.WIDTH
            )
        pixel_width = (
            self._field.width() * CellWidget.CELL_SIZE
            + (self._field.width() - 1) * WallWidget.WIDTH
            )
        
        field_surface = pg.Surface((pixel_width, pixel_height))

        for row in range(self._field.height()):
            for col in range(self._field.width()):
                cell = self._field.get_cell(col, row)
                cell_widget = self._widget_factory.create(cell)

                x = col * CellWidget.CELL_SIZE + col * WallWidget.WIDTH
                y = row * CellWidget.CELL_SIZE + row * WallWidget.WIDTH
                field_surface.blit(cell_widget.render(), (x, y))

                # Особенность отрисовки стен заключается в следующем:
                # Если имееются две клетки, A и B, которые являются соседями друг друга,
                # причем клетка A сосед B с севера, то значит, что B сосед A с юга.
                # Пусть между ними стоит стена. Цикл ниже будет отрисовывать одну и ту же стену два раза:
                # сначала, как с севереного направления клетки A, а потом как с южного направления клетки B.
                # Является ли это багом или фичей вопрос открытый, но отрисовка выглядит хорошо
                for direction, wall in cell.walls().items():
                    wall_widget = self._widget_factory.create(wall)
                    match direction:
                        case Direction.NORTH:
                            wall_x = x
                            wall_y = y - WallWidget.WIDTH
                        case Direction.WEST:
                            wall_x = x - WallWidget.WIDTH
                            wall_y = y - WallWidget.WIDTH
                        case Direction.SOUTH:
                            wall_x = x - WallWidget.WIDTH
                            wall_y = y + WallWidget.LENGTH - WallWidget.WIDTH
                        case Direction.EAST:
                            wall_x = x + WallWidget.LENGTH - WallWidget.WIDTH
                            wall_y = y
                    field_surface.blit(wall_widget.render(), (wall_x, wall_y))

        return field_surface
    
    def size(self) -> tuple[int, int]:
        pixel_width = self._field.width() * CellWidget.CELL_SIZE + (self._field.width() - 1) * WallWidget.WIDTH
        pixel_height = self._field.height() * CellWidget.CELL_SIZE + (self._field.height() - 1) * WallWidget.WIDTH
        return (pixel_width, pixel_height)

    @override
    def render(self) -> pg.Surface:
        return self._make_field_surface()

    @override
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        from_cell_widget = self._widget_factory.create(from_cell)
        to_cell_widget = self._widget_factory.create(to_cell)
        robot_widget = self._widget_factory.create(robot)
        from_cell_widget.remove_item_widget(robot_widget)
        to_cell_widget.add_item_widget(robot_widget)

    @override
    def on_robot_not_moved(self, robot: Robot) -> None:
        pass

    @override
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        pass