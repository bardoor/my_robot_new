from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.ui.core.widget import Widget


if TYPE_CHECKING:
    from robot.model.direction import Direction


class WallWidget(Widget):

    def __init__(self, direction: Direction) -> None:
        self._direction = direction
    