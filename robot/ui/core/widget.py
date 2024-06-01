from abc import ABC, abstractmethod

import pygame as pg


class Widget(ABC):

    @abstractmethod
    def render(self) -> pg.Surface:
        ... 