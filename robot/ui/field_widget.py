from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.ui.core import Widget


if TYPE_CHECKING:
    from robot.model.field import Robot, Field


class FieldWidget(Widget, RobotListener):

    def __init__(self, field: Field) -> None:
        self._field = field
        self._surface = self._make_field_surface()

    def _make_filed_surface(self):
        ...