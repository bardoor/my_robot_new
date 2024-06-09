import threading
import sys
from sys import exc_info
from traceback import format_exception
from tkinter import filedialog as fd
import os
import signal

import pygame

from robot.model.field import dump_field, load_field
from robot.ui.core import Widget


class GUI(threading.Thread):
    instantiated = False # Attempt to prevent the user from running multiple at once

    def __init__(self, main_window: Widget, server_pid: int, fps: int = 30) -> None:
        if GUI.instantiated:
            raise RuntimeError("Only one GUI may run at a time")
        threading.Thread.__init__(self) # Run the Thread parent init
        GUI.instantiated = True # Limit one running at once

        self.main_window = main_window
        self.server_pid = server_pid
        self.fps = fps
        self.running = True
        self.error = None
        self.display_size = self.main_window.size()

        # Start the thread, which starts the loop
        self.start()

    def run(self):
        """ The function that is Threaded. DO NOT call this function."""
        # Set up Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()
        self.field = self.main_window.field()
        self.field_widget = self.main_window.field_widget()

        closed_window = False
        # Start the main game loop
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        dump_field(self.field, "output")
                        pygame.quit()
                        closed_window = True
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            filename = fd.asksaveasfilename(title="Сохранить обстановку", filetypes=(('Файл обстановки', '.json'),))
                            dump_field(self.field, filename)
                        elif event.key == pygame.K_o:
                            path = fd.askopenfilename(title="Загрузить обстановку", filetypes=(('Файл обстановки', '.json'),))
                            self.field_widget.set_field(load_field(path))

                    self.main_window.handle_event(event)

                if closed_window:
                    break

                self.main_window.update()
                if self.main_window.size() != self.display_size:
                    self.display_size = self.main_window.size()
                    self.screen = pygame.display.set_mode(self.main_window.size())
                self.screen.blit(self.main_window.render(), (0, 0))
                pygame.display.flip()
        except: # Fail gracefully instead of freezing if we have an error
            self.error = "".join(format_exception(*exc_info()))
            print(self.error)
            self.running = False
        # Below will be executed whenever the thread quits gracefully or kill is called
        pygame.quit()
        print(self.server_pid, file=sys.stderr)
        #os.kill(self.server_pid, signal.SIGTERM)
        GUI.instantiated = False
        print(423423423)
        return self.error

    def kill(self):
        """ Gracefully halt the thread and shutdown Pygame.
            Calling del on a ThreadedRenderer will not do close the window,
            just decrement its reference count, as the Thread is still running.
            
            This leaves behind a stopped thread object. You may still access
            its variables, but since it inherits from threading.Thread,
            start may not be called on it again, and calling run will not start
            a new thread."""
        self.running = False