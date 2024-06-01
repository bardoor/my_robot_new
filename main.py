import pygame
import sys

from robot.model.field import Cell
from robot.model.robot import Robot
from robot.ui.field.cell_widget import CellWidget


pygame.init()

screen = pygame.display.set_mode((1000, 800))

cell_1 = Cell()
cell_2 = Cell()
robot = Robot()
robot.set_cell(cell_1)

cell_widget_1 = CellWidget(cell_1)
cell_widget_2 = CellWidget(cell_2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            cell_1.paint()

    screen.blit(cell_widget_1.render(), (0, 0))

    pygame.display.update()
    