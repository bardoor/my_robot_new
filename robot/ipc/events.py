from enum import IntEnum, auto

import pygame as pg


class EventType(IntEnum):
    # События для графического интерфейса
    RELOAD_FIELD = pg.USEREVENT + 1
    # Робот успешно завершил исполнение команд
    # TODO: FINISHED_EXECUTION = auto() 
    # Робот разбился
    # TODO: INTERRUPTED_EXECUTION = auto() 

    # События для сервера
    STOP_RUNNING_SERVER = auto()
    SET_ROBOT = auto()


def Event(event_type: EventType, **props) -> pg.event.Event:
    return pg.event.Event(event_type, **props)
