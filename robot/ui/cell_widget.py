from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event.listeners import CellListener
from robot.ui.core.widget import Widget


if TYPE_CHECKING:
    from robot.model.field import Cell
    from robot.model.robot import Robot


class CellWidget(Widget, CellListener):
    CELL_SIZE = 80
    UNPAINTED_COLOR = pg.color.THECOLORS['white']
    PAINTED_COLOR = pg.color.THECOLORS['cyan']

    def __init__(self, cell: Cell) -> None:
        self._cell = cell
        self._cell.add_listener(self)
        self._item_widget = None

    def add_item_widget(self, widget: Widget) -> None:
        if self._item_widget is not None:
            raise ValueError("Already has a widget inside")        
        self._item_widget = widget

    def remove_item_widget(self, widget: Widget) -> None:
        # Не знаю, насколько это хорошая идея, передавать в 
        # качестве параметра виджет, который мы хотим удалить из себя,
        # но возможно в будущем клетка сможет хранить более одного виджета
        if self._item_widget is not None and self._item_widget != widget:
            raise ValueError("Given widget is not in CellWidget")
        self._item_widget = None

    def _make_cell_surface(self) -> pg.Surface:
        surface = pg.Surface((CellWidget.CELL_SIZE, CellWidget.CELL_SIZE))
        surface.fill(
            CellWidget.PAINTED_COLOR if self._cell.is_painted() else CellWidget.UNPAINTED_COLOR
        )

        if self._item_widget is not None:
            # (x, y)
            center = [CellWidget.CELL_SIZE // 2, CellWidget.CELL_SIZE // 2]
            
            # Сдвигаем координаты так, чтобы отрисовать виджет айтема по центру
            item_size = self._item_widget.size()
            center[0] -= item_size[0] // 2
            center[1] -= item_size[1] // 2

            surface.blit(self._item_widget.render(), center)

        return surface

    @override
    def on_cell_got_painted(self, cell: Cell) -> None:
        pass

    @override
    def on_robot_left_cell(self, robot: Robot, left_cell: Cell) -> None:
        pass

    @override
    def on_robot_arrived_in_cell(self, robot: Robot, arrived_cell: Cell) -> None:
        pass

    @override
    def render(self) -> pg.Surface:
        return self._make_cell_surface()

    @override
    def update(self):
        pass

    @override
    def handle_events(self, events: pg.event.Event):
        pass
    