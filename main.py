import pygame
import sys
from tkinter import filedialog as fd
from robot.model.field import load_field, dump_field
from robot.model.direction import Direction
from robot.ui import FieldWidget
from robot.ui.backing_widget import BackingWidget
from robot.ui.main_window import MainWindow

pygame.init()

field = load_field("field")
field_widget = FieldWidget(field)
main_window = MainWindow(BackingWidget(field_widget))

size = main_window.size()
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dump_field(field, "output")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                field.robot().step(Direction.WEST)
            elif event.key == pygame.K_UP:
                field.robot().step(Direction.NORTH)
            elif event.key == pygame.K_DOWN:
                field.robot().step(Direction.SOUTH)
            elif event.key == pygame.K_RIGHT:
                field.robot().step(Direction.EAST)
            elif event.key == pygame.K_SPACE:
                field.robot().paint()
            elif event.key == pygame.K_s:
                filename = fd.asksaveasfilename(title="Сохранить обстановку", filetypes=(('Файл обстановки', '.json'),))
                dump_field(field, filename)
            elif event.key == pygame.K_o:
                path = fd.askopenfilename(title="Загрузить обстановку", filetypes=(('Файл обстановки', '.json'),))
                field_widget.set_field(load_field(path))

        main_window.handle_event(event)

    main_window.update()
    if main_window.size() != size:
        size = main_window.size()
        screen = pygame.display.set_mode(main_window.size())
    screen.blit(main_window.render(), (0, 0))
    pygame.display.flip()
