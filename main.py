import pygame
import sys

from robot.model.field import load_field, dump_field
from robot.model.direction import Direction
from robot.ui import FieldWidget


pygame.init()

field = load_field("field")
field_widget = FieldWidget(field)

screen = pygame.display.set_mode(field_widget.size())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dump_field(field, "output")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                field.robot().step(Direction.WEST)
            elif event.key == pygame.K_w:
                field.robot().step(Direction.NORTH)
            elif event.key == pygame.K_s:
                field.robot().step(Direction.SOUTH)
            elif event.key == pygame.K_d:
                field.robot().step(Direction.EAST)
            elif event.key == pygame.K_SPACE:
                field.robot().paint()
    
    screen.blit(field_widget.render(), (0, 0))
    pygame.display.flip()