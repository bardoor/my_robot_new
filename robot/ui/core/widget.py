from abc import ABC, abstractmethod

import pygame as pg


class Widget(ABC):

    def size(self) -> tuple[int, int]:
        return self.render().get_size()

    @abstractmethod
    def render(self) -> pg.Surface:
        ... 