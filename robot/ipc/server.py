from __future__ import annotations
from typing import TYPE_CHECKING
import socket
from threading import Thread
import select
from queue import Queue

from robot.ipc.config import Config
from robot.ipc.parser import parse
from robot.ipc.socket_json import send_json, recv_json
from robot.ui import *
from robot.ipc.program import Program
from robot.model.robot.robot import StepResult
from robot.model.robot.robot_command import *
from robot.ipc.utils import is_process_alive
from .events import *


class Server(Thread):
    '''Реализует взаимодействие между клиентом (т.е. IDE, скриптом и т.д.) и моделью.'''

    def __init__(self,
                 ui_events_queue: Queue,
                 server_events_queue: Queue,
                 ) -> None:
        '''
        :param ui_events_queue: Очередь событий графического окна.
        :param server_events_queue: Очередь событий сервера.
        '''
        super().__init__()

        self._ui_events_queue = ui_events_queue
        self._server_events_queue = server_events_queue

        # Сокет сервера
        self._server = socket.socket()
        self._server.bind((Config.HOST, Config.PORT))
        self._server.listen(1)

        # Сокет клиента и его адрес
        self._client = None
        self._client_addr = None
        # Идентификатор процесса клиента (используется
        # для отслеживания состояние процесса - жив или нет)
        self._client_pid = None

        # Флаг, показывающий, работает ли сервер
        self._running = True

        # Интервал исполнения команд
        self._exec_interval = Config.EXEC_INTERVAL

        # Связь с моделью: программа (контейнер команд) и робот
        self._program = None
        self._robot = None

    def run(self) -> None:
        '''Цикл обработки сервера.'''
        while self._running:
            # Обрабатываем события, поступившие к серверу от интерфейса
            # (в ходе обработки событий интерфейс может потребовать от сервера прекратить
            # обрабатывать команды, поэтому необходимо проверить, а надо ли это делать дальше)
            self._handle_event()
            if not self._running:
                break

            # Если к серверу еще никто не подключился, пытается кого-нибудь подключить.
            # В случае успешного подключения отправляем интерфейсу событие на перезагрузку поля
            # и дожидаемся того, как интерфейс его обработает (командам необходим исполнитель - 
            # робот - а его можно получить только если поле было загружено)
            if self._client is None:
                if self._accept():
                    reload_field_event = Event(EventType.RELOAD_FIELD)
                    self._ui_events_queue.put(reload_field_event)
                    self._ui_events_queue.join()
                continue

            # Далее мы обрабатываем по одному запросу от клиента
            self._process_request()

            # После обработки запроса проверяем, не отключился ли клиент
            # (как только все команды выполнились, процесс клиента умирает)
            if not is_process_alive(self._client_pid):
                self._close()

        self._server.close()
        self._server = None

    def _accept(self) -> bool:
        '''
        Реализация неблокирующего соединения с клиентским сокетом.

        :return: `True` если соединение установлено, `False` иначе.
        '''
        inputs = [self._server]
        outputs = []
        readable, _, _ = select.select(inputs, outputs, inputs, 1)

        if not readable:
            return False
        
        for sock in readable:
            if sock == self._server:
                self._client, self._client_addr = self._server.accept()
                break

        return True

    def _close(self) -> None:
        '''
        Очистка ресурсов: закрывает соединение с клиентским сокетом
        и очищает программу с роботом.
        Может быть вызвана, если клиентский соект не подключен.
        '''
        if self._program is not None:
            self._program.end_execution()
            self._program = None
            self._robot = None
        if self._client is not None:
            self._client.close()
            self._client = None
            self._client_addr = None
            self._client_pid = None

    def _process_request(self) -> None:
        '''
        Обработка клиентского запроса (команды для робота).
        '''
        started_execution = False
        request = self._receive_request()
        match request:
            case {'command': 'register', 'pid': client_pid}:
                self._client_pid = client_pid
                self._send_response(status='registered')
            case {'command': _}:
                if not started_execution:
                    self._program.start_execution(self._exec_interval)
                    started_execution = True
                parsed_request = parse(request)
                self._program.add_command(parsed_request)
                result = self._program.get_result()
                self._send_command_result(parsed_request, result)
            case _:
                raise RuntimeError(f'Unsupported request: {request}')

    def _handle_event(self) -> None:
        '''
        Обработка событий, посланных серверу.
        '''
        while not self._server_events_queue.empty():
            event = self._server_events_queue.get()
            match event.type:
                case EventType.STOP_RUNNING_SERVER:
                    self._running = False
                    self._close()
                case EventType.SET_ROBOT:
                    self._robot = event.robot
                    self._program = Program(self._robot)
                case _:
                    raise ValueError(f'[SERVER]: cannot handle event: {event.type}')
            self._server_events_queue.task_done()

    def _receive_request(self) -> dict:
        '''Обертка для получения данных от клиента'''
        return recv_json(self._client)

    def _send_response(self, **response_data) -> None:
        '''
        Обертка для отправления данных клиенту.

        :param response_data: Дополнительные атрибуты ответа.
        '''
        send_json(self._client, response_data)

    def _send_command_result(self, command: RobotCommand, result=None) -> None:
        if isinstance(command, Step):
            match result:
                case StepResult.OK:
                    status = "executed"
                case StepResult.NOT_MOVED | StepResult.HIT_WALL:
                    status = "crashed"
                case _:
                    print(f'RESULT {result}')
                    raise ValueError
        elif isinstance(command, Paint):
            status = "executed"
        elif isinstance(command, CheckWall):
            status = "executed"
        else:
            raise ValueError

        if isinstance(result, bool):
            self._send_response(status=status, result=result)
        else:
            self._send_response(status=status)
