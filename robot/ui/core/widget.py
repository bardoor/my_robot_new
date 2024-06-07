from abc import ABC, abstractmethod

import pygame as pg


class Widget(ABC):

    def size(self) -> tuple[int, int]:
        """Возвращает размер виджета в виде кортежа (ширина, высота)"""
        return self.render().get_size()

    @abstractmethod
    def render(self) -> pg.Surface:
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def on_click(self):
        ...
