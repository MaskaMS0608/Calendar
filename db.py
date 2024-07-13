from typing import List

import model
import storage


class DBException(Exception):
    pass


class EventDB:
    def __init__(self):
        self._storage = storage.LocalStorage()

    def create(self, event: model.Event) -> str:
        try:
            return self._storage.create(event)
        except Exception as ex:
            raise DBException(f"failed CREATE operation with: {ex}")

    def list(self) -> List[model.Event]:
        try:
            return self._storage.list()
        except Exception as ex:
            raise DBException(f"failed LIST operation with: {ex}")

    def read(self, _id: str) -> model.Event:
        try:
            return self._storage.read(_id)
        except Exception as ex:
            raise DBException(f"failed READ operation with: {ex}")

    def update(self, _id: str, event: model.Event):
        try:
            return self._storage.update(_id, event)
        except Exception as ex:
            raise DBException(f"failed UPDATE operation with: {ex}")

    def delete(self, _id: str):
        try:
            return self._storage.delete(_id)
        except Exception as ex:
            raise DBException(f"failed DELETE operation with: {ex}")


"""
Этот код определяет класс EventDB, который предоставляет методы для работы с базой данных событий. 
Класс использует модули model и storage для взаимодействия с данными.
Метод init инициализирует экземпляр класса, устанавливая ссылку на объект LocalStorage из модуля storage.
Методы create, list, read, update и delete предоставляют функциональность CRUD 
(создание, чтение, обновление, удаление) для работы с событиями. 
Каждый из этих методов вызывает соответствующий метод объекта LocalStorage, который выполняет операцию с базой данных.
Если при выполнении операции возникает исключение, класс DBException используется для обработки ошибки и генерации сообщения об ошибке."""
