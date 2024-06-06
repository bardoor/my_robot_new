from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.model.direction import Direction
from robot.ui.core import Widget
from robot.ui.cell_widget import CellWidget
from robot.ui.field_widget import FieldWidget
from robot.ui.widget_factory import WidgetFactory

if TYPE_CHECKING:
    from robot.model.field import Field, Cell
    from robot.model.robot import Robot


class BackingWidget(Widget):
    MARGIN = 70
    COLOR = pg.color.THECOLORS['coral1']

    def __init__(self, field: FieldWidget):
        self._field = field

    def render(self) -> pg.Surface:
        field_w, field_h = self._field.size()
        backing_w, backing_h = field_w + BackingWidget.MARGIN, field_h + BackingWidget.MARGIN

        surface = pg.Surface((backing_w, backing_h))
        surface.fill(BackingWidget.COLOR)

        if self._field is not None:
            center = [backing_w // 2, backing_h // 2]

            # Сдвигаем координаты так, чтобы отрисовать виджет айтема по центру
            center[0] -= field_w // 2
            center[1] -= field_h // 2

            surface.blit(self._field.render(), center)

        return surface
