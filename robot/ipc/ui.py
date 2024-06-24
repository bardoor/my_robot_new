from tkinter import filedialog as fd
from tkinter import messagebox as mb
from typing import NoReturn
from queue import Queue
import os

import pygame as pg

from robot.model.field import Field
from robot.serialize import (
    load_field_from_json,
    load_field_from_dict,
    dump_field_to_json,
)
from robot.ui import (
    FieldWidget,
    BackingWidget,
    MainWindow,
)
from robot.ipc.server import Server
from .events import *


def _create_main_window(field: Field) -> MainWindow:
    field_widget = FieldWidget(field)
    backing_widget = BackingWidget(field_widget)
    main_window = MainWindow(backing_widget)
    return main_window


def _create_main_window_from_json(file_name: str) -> MainWindow:
    field = load_field_from_json(file_name)
    return _create_main_window(field)


def _create_default_main_window() -> MainWindow:
    field = load_field_from_dict(
        {
            'height': 5,
            'width': 5,
            'robot': {'x': 0, 'y': 0},
        }
    )
    return _create_main_window(field)


class UI:
    '''Графическое окно.'''

    def __init__(self, fps: int = 30) -> None:
        self._fps = fps
        self._screen = None
        self._current_widget = None
        self._clock = pg.time.Clock()

        # Путь к файлу, содержащему текущую обстановку
        # (None, если задействована обстановка по умолчанию)
        self._current_field_path = None

        # Очередь событий графического окна
        self._ui_events_queue = Queue()
        # Очередь событий сервера
        self._server_events_queue = Queue()

        self._server = Server(self._ui_events_queue, self._server_events_queue)

    def mainloop(self) -> NoReturn:
        '''Цикл обработки графического окна.'''
        pg.init()

        self._load_field()

        self._server.start()

        self._running = True
        while self._running:
            # После обработки событий необходимо проверять,
            # нужно ли дальше выполнять команды.
            self._handle_event()
            if not self._running:
                break

            self._render()

        self._exit()

    def _reload_field(self) -> None:
        '''Перезагружает текущую обстановку.'''
        self._load_field(self._current_field_path)

    def _load_field(self, file_name: str | None = None) -> None:
        '''
        Загружает новую обстановку по файлу или обстановку по умолчанию

        :param file_name: Имя файла обстановки, `None` если нужно загрузить обстановку по умолчанию.
        '''
        if file_name is None:
            self._current_widget = _create_default_main_window()
            self._current_field_path = None
        else:
            self._current_widget = _create_main_window_from_json(file_name)
            self._current_field_path = file_name

        self._screen = pg.display.set_mode(self._current_widget.size())

    def _load_field_dialog(self) -> None:
        '''Открывает диалоговое окно для загрузки обстановки.'''
        path = fd.askopenfilename(
            title="Загрузить обстановку",
            filetypes=[('Файл обстановки', '.json')],
            )
        
        if not path: return
        
        self._load_field(path)

    def _save_field(self, file_name: str) -> None:
        '''
        Сохраняет текущее поле в файле.

        :param file_name: Имя файла обстановки.
        '''
        dump_field_to_json(self._current_widget.field(), file_name)

    def _save_field_dialog(self) -> None:
        '''Открывает диалоговое окно для сохранения обстановки.'''
        path = fd.asksaveasfilename(
            title="Сохранить обстановку",
            filetypes=[('Файл обстановки', '.json')],
            )
        
        if not path: return
        
        self._save_field(path)

    def _exit(self) -> NoReturn:
        '''Осуществляет выход из приложения, убивая поток сервера и закрывая графическое окно'''
        # Отправляем серверу событие завершения работы
        self._server_events_queue.put(Event(EventType.STOP_RUNNING_SERVER))
        self._server_events_queue.join()
        self._server.join()

        self._running = False

        pg.quit()
        os._exit(0)

    def _render(self) -> None:
        '''Отрисовывает поле.'''
        self._screen.blit(self._current_widget.render(), (0, 0))
        pg.display.flip()
        self._clock.tick(self._fps)

    def _handle_event(self) -> None:
        '''Обработка событий в очереди графического окна и событий pygame'''
        while not self._ui_events_queue.empty():
            event = self._ui_events_queue.get()
            match event.type:
                case EventType.RELOAD_FIELD:
                    self._reload_field()
                    robot_event = Event(EventType.SET_ROBOT, robot=self._current_widget.field().robot())
                    self._server_events_queue.put(robot_event)
                case _:
                    raise ValueError(f'[UI]: cannot handle event: {event.type}')
            self._ui_events_queue.task_done()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._running = False
                case pg.KEYDOWN:
                    match event.key:
                        case pg.K_s:
                            self._save_field_dialog()
                        case pg.K_o:
                            self._load_field_dialog()
