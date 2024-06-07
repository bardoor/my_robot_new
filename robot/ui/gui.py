import threading
from sys import exc_info
from traceback import format_exception

import pygame

from robot.ui.core import Widget


class GUI(threading.Thread):
    instantiated = False # Attempt to prevent the user from running multiple at once

    def __init__(self, main_widget: Widget, fps: int = 30) -> None:
        if GUI.instantiated:
            raise RuntimeError("Only one GUI may run at a time")
        threading.Thread.__init__(self) # Run the Thread parent init
        GUI.instantiated = True # Limit one running at once

        self.main_widget = main_widget
        self.fps = fps
        self.running = True
        self.error = None
        self.display_size = self.main_widget.size()

        # Start the thread, which starts the loop
        self.start()

    def run(self):
        """ The function that is Threaded. DO NOT call this function."""
        # Set up Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()

        # Start the main game loop
        try:
            while self.running is True:
                self.clock.tick(self.fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: # May be overridden
                        self.running = False
                self.screen.blit(self.main_widget.render(), (0, 0))
                pygame.display.flip()
        except: # Fail gracefully instead of freezing if we have an error
            self.error = "".join(format_exception(*exc_info()))
            print(self.error)
            self.running = False
        # Below will be executed whenever the thread quits gracefully or kill is called
        pygame.quit()
        GUI.instantiated = False
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
