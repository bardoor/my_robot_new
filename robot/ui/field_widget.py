from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.ui.core import Widget
from robot.ui.cell_widget import CellWidget
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
            + (self._field.height() - 1) * FieldWidget.GAP
            )
        pixel_width = (
            self._field.width() * CellWidget.CELL_SIZE
            + (self._field.width() - 1) * FieldWidget.GAP
            )
        
        field_surface = pg.Surface((pixel_width, pixel_height))

        for row in range(self._field.height()):
            for col in range(self._field.width()):
                cell_widget = self._widget_factory.create(self._field.get_cell(col, row))

                x = col * CellWidget.CELL_SIZE + col * FieldWidget.GAP
                y = row * CellWidget.CELL_SIZE + row * FieldWidget.GAP
                field_surface.blit(cell_widget.render(), (x, y))

        return field_surface
    
    def size(self) -> tuple[int, int]:
        pixel_width = self._field.width() * CellWidget.CELL_SIZE + (self._field.width() - 1) * FieldWidget.GAP
        pixel_height = self._field.height() * CellWidget.CELL_SIZE + (self._field.height() - 1) * FieldWidget.GAP
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