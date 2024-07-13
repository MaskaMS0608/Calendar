from typing import List
from datetime import datetime, timedelta
import model
import db

# максимальная длина заголовка — 30 символов
# максимальная длина поля Текст — 200 символов
TITLE_LIMIT = 30
TEXT_LIMIT = 200


class EventException(Exception):
    pass


class EventLogic:
    def __init__(self):
        self._event_db = db.EventDB()

    @staticmethod
    def _validate_event(event: model.Event):
        if event is None:
            raise EventException("event is None")
        if event.title is None or len(event.title) > TITLE_LIMIT:
            raise EventException(f"title length > MAX: {TITLE_LIMIT}")
        if event.text is None or len(event.text) > TEXT_LIMIT:
            raise EventException(f"text length > MAX: {TEXT_LIMIT}")

        # Проверка на создание одной заметки в день
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        if datetime(event.date) >= datetime(yesterday):
            raise EventException(f"Not allowed to create more than one note per day.")

    def create(self, event: model.Event) -> str:
        self._validate_event(event)
        try:
            return self._event_db.create(event)
        except Exception as ex:
            raise EventException(f"failed CREATE operation with: {ex}")

    def list(self) -> List[model.Event]:
        try:
            return self._event_db.list()
        except Exception as ex:
            raise EventException(f"failed LIST operation with: {ex}")

    def read(self, _id: str) -> model.Event:
        try:
            return self._event_db.read(_id)
        except Exception as ex:
            raise EventException(f"failed READ operation with: {ex}")

    def update(self, _id: str, event: model.Event):
        self._validate_event(event)
        try:
            return self._event_db.update(_id, event)
        except Exception as ex:
            raise EventException(f"failed UPDATE operation with: {ex}")

    def delete(self, _id: str):
        try:
            return self._event_db.delete(_id)
        except Exception as ex:
            raise EventException(f"failed DELETE operation with: {ex}")


"""
Этот код определяет класс EventLogic, который предоставляет логику для работы с событиями. 
Класс использует класс EventDB из модуля db для доступа к базе данных.
Метод init инициализирует экземпляр класса, устанавливая ссылку на объект EventDB.
Методы create, list, read, update и delete предоставляют функциональность CRUD для работы с событиями. 
Каждый из этих методов вызывает соответствующий метод объекта EventDB, который затем выполняет операцию с базой данных.
Перед выполнением любой операции с событием, метод _validate_event проверяет корректность предоставленных данных. 
Он проверяет, что событие не является None, что длина заголовка и текста не превышают установленные ограничения, и что событие не создается чаще одного раза в день.
Если при выполнении операции возникает исключение, класс EventException используется для обработки ошибки и генерации сообщения об ошибке."""
