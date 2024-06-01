from typing import override

import pygame as pg

from robot.model.field import Cell
from robot.model.event.listeners import CellListener
from robot.ui.field.widget import Widget


class CellWidget(Widget, CellListener):
    CELL_SIZE = 80
    UNPAINTED_COLOR = pg.color.THECOLORS['white']
    PAINTED_COLOR = pg.color.THECOLORS['cyan']

    def __init__(self, cell: Cell) -> None:
        self._cell = cell
        self._cell.add_listener(self)
        self._surface = self._make_cell_surface()
        self._item_widget = None

    def add_item_widget(self, widget: Widget) -> None:
        if self._item_widget is not None:
            raise ValueError("Already has a widget inside")        
        self._item_widget = widget

    def _make_cell_surface(self) -> pg.Surface:
        surface = pg.Surface((CellWidget.CELL_SIZE, CellWidget.CELL_SIZE))
        surface.fill(
            CellWidget.PAINTED_COLOR if self._cell.is_painted() else CellWidget.UNPAINTED_COLOR
        )
        return surface

    @override
    def on_cell_got_painted(self) -> None:
        self._surface.fill(CellWidget.PAINTED_COLOR)

    @override
    def on_robot_left_cell(self) -> None:
        self._surface = self._make_cell_surface()

    @override
    def on_robot_arrived_in_cell(self) -> None:
        center = (CellWidget.CELL_SIZE // 2, CellWidget.CELL_SIZE // 2)
        self._surface.blit(self._item_widget.render(), center)

    @override
    def render(self) -> pg.Surface:
        return self._surface
    