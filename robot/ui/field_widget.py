from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.model.direction import Direction
from robot.ui.core import Widget
from robot.ui.cell_widget import CellWidget
from robot.ui.wall_widget import WallWidget
from robot.ui.widget_factory import WidgetFactory

if TYPE_CHECKING:
    from robot.model.field import Field, Cell
    from robot.model.robot import Robot


class FieldWidget(Widget, RobotListener):
    def __init__(self, field: Field) -> None:
        self._field = field
        self._widget_factory = WidgetFactory()
        self._widgets = {}
        self._edit_mode = False

        if self._field.robot() is not None:
            self._field.robot().add_listener(self)

    def _make_field_surface(self) -> pg.Surface:
        pixel_height = (
                self._field.height() * CellWidget.CELL_SIZE
                + (self._field.height() - 1) * WallWidget.WIDTH
        )
        pixel_width = (
                self._field.width() * CellWidget.CELL_SIZE
                + (self._field.width() - 1) * WallWidget.WIDTH
        )

        field_surface = pg.Surface((pixel_width, pixel_height))

        seen_walls = set()
        for row in range(self._field.height()):
            for col in range(self._field.width()):
                cell = self._field.get_cell(col, row)
                cell_widget = self._widget_factory.create(cell)

                x = col * CellWidget.CELL_SIZE + col * WallWidget.WIDTH
                y = row * CellWidget.CELL_SIZE + row * WallWidget.WIDTH
                self._widgets[cell_widget] = (x, y)
                field_surface.blit(cell_widget.render(), (x, y))

                for direction in Direction.every():
                    match direction:
                        case Direction.NORTH:
                            wall_x = x
                            wall_y = y - WallWidget.WIDTH
                        case Direction.WEST:
                            wall_x = x - WallWidget.WIDTH
                            wall_y = y - WallWidget.WIDTH
                        case Direction.SOUTH:
                            wall_x = x - WallWidget.WIDTH
                            wall_y = y + WallWidget.LENGTH - WallWidget.WIDTH
                        case Direction.EAST:
                            wall_x = x + WallWidget.LENGTH - WallWidget.WIDTH
                            wall_y = y

                    if not cell.has_wall(direction):
                        wall_widget = self._widget_factory.create_blank_wall(cell, direction)
                    else:
                        wall = cell.get_wall(direction)
                        if wall in seen_walls:
                            continue
                        seen_walls.add(wall)
                        wall_widget = self._widget_factory.create(wall)

                    self._widgets[wall_widget] = (wall_x, wall_y)
                    field_surface.blit(wall_widget.render(), (wall_x, wall_y))

        return field_surface

    @override
    def size(self) -> tuple[int, int]:
        pixel_width = self._field.width() * CellWidget.CELL_SIZE + (self._field.width() - 1) * WallWidget.WIDTH
        pixel_height = self._field.height() * CellWidget.CELL_SIZE + (self._field.height() - 1) * WallWidget.WIDTH
        return (pixel_width, pixel_height)

    @override
    def render(self) -> pg.Surface:
        return self._make_field_surface()

    @override
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        from_cell_widget = self._widget_factory.create(from_cell)
        to_cell_widget = self._widget_factory.create(to_cell)
        robot_widget = self._widget_factory.create(robot)
        from_cell_widget.remove_item_widget(robot_widget)
        to_cell_widget.add_item_widget(robot_widget)

    @override
    def on_robot_crashed(self, robot: Robot) -> None:
        pass

    @override
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        pass

    def set_edit_mode(self, value: bool):
        self._edit_mode = value
        self._field.set_edit_mode(value)

    @override
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN and event.key == pg.K_e:
            self.set_edit_mode(not self._edit_mode)

        if self._edit_mode is False:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r and pg.key.get_mods() & pg.KMOD_CTRL:
                self._field.remove_row()
            elif event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
                self._field.remove_col()
            elif event.key == pg.K_r:
                self._field.add_row()
            elif event.key == pg.K_c:
                self._field.add_col()
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            clicked_widget = self._get_widget(pos)
            if clicked_widget is not None:
                self._get_widget(pos).handle_event(event)


    def _get_widget(self, pos: tuple[int, int]):
        for widget, widget_pos in self._widgets.items():
            if widget.collidepoint(widget_pos, pos):
                return widget

    @override
    def update(self):
        pass
