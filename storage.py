from typing import List
import model


class StorageException(Exception):
    pass


class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create(self, event: model.Event) -> str:
        self._id_counter += 1
        event.id = str(self._id_counter)
        self._storage[event.id] = event
        return event.id

    def list(self) -> List[model.Event]:
        return list(self._storage.values())

    def read(self, _id: str) -> model.Event:
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, event: model.Event):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        event.id = _id
        self._storage[event.id] = event

    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]


"""
Этот код определяет класс LocalStorage, который представляет собой простую реализацию хранилища данных для событий. 
Класс использует класс model.Event для представления событий.
Метод init инициализирует экземпляр класса, устанавливая счетчик идентификаторов и пустое словарное значение для хранения событий.
Метод create увеличивает счетчик идентификаторов, присваивает новый идентификатор событию и добавляет его в словарь хранения.
Методы list, read, update и delete предоставляют функциональность CRUD для работы с событиями. 
Они используют словарь _storage для доступа к данным.
Если при выполнении операции возникает исключение, 
класс StorageException используется для обработки ошибки и генерации сообщения об ошибке."""
