from typing import override

import pygame as pg

from robot.model.field import Robot, Field
from robot.model.event.listeners import RobotListener
from robot.ui.field.widget import Widget


class FieldWidget(Widget, RobotListener):

    def __init__(self, field: Field) -> None:
        self._field = field
        self._surface = self._make_field_surface()

    def _make_filed_surface(self):
        ...