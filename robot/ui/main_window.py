from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.field import Field, load_field
from robot.ui.core import Widget
from robot.ui.field_widget import FieldWidget
from robot.ui.backing_widget import BackingWidget


class MainWindow(Widget):
    def __init__(self, backing: BackingWidget):
        self._backing = backing

    # Юзать будем когда роботом станет управлять программа а не стрелки
    def _handle_events(self):
        events = pg.event.get()
        for event in events:
            self._backing.handle_event(event)

    def render(self) -> pg.Surface:
        return self._backing.render()

    def update(self):
        self._handle_events()

    def handle_event(self, event: pg.event.Event):
        self._backing.handle_event(event)
