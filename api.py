from datetime import datetime
import model
from model import Event
import logic

from flask import Flask
from flask import request

app = Flask(__name__)

_event_logic = logic.EventLogic()


class ApiException(Exception):
    pass


def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split("|")
    if len(parts) == 3:
        event = model.Event()
        event.id = None
        event.date = datetime.strptime(parts[0], "%Y-%m-%d").date()
        event.title = parts[1]
        event.text = parts[2]
        return event
    elif len(parts) == 4:
        event = model.Event()
        event.id = parts[0]
        event.date = datetime.strptime(parts[1], "%Y-%m-%d").date()
        event.title = parts[2]
        event.text = parts[3]
        return event
    else:
        raise ApiException(f"invalid RAW event data {raw_event}")


def _to_raw(event: model.Event) -> str:
    if event.id is None:
        return f"{event.date}|{event.title}|{event.text}"
    else:
        return f"{event.id}|{event.date}|{event.title}|{event.text}"


# API интерфейс: /api/v1/calendar/…
API_ROOT = "/api/v1/calendar"
EVENT_API_ROOT = API_ROOT + "/event"


@app.route(API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode("utf-8")
        event = _from_raw(data)
        id = _event_logic.create(event)
        return f"new id: {id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/", methods=["GET"])
def list_():
    try:
        events = _event_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + "\n"
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["GET"])
def read(_id: str):
    try:
        event = _event_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode("utf-8")
        event = _from_raw(data)
        _event_logic.update(_id, event)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _event_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404


if __name__ == "__main__":
    app.run(debug=True)

"""
Код представляет собой веб-приложение, написанное на Python с использованием фреймворка Flask. 
Это приложение предоставляет RESTful API для управления событиями. Пользователь может создавать, читать, обновлять и удалять события через HTTP-запросы.
Класс ApiException используется для обработки исключений, которые могут возникнуть при работе с API. 
Функции _from_raw и _to_raw используются для преобразования данных между форматами.
Маршрутизация запросов осуществляется с помощью декораторов @app.route. 
Например, метод create принимает POST-запрос к маршруту /api/v1/calendar/event/ и создает новое событие. 
Метод list_ принимает GET-запрос к тому же маршруту и возвращает список всех событий. 
Методы read, update и delete работают аналогично, но принимают разные методы HTTP и параметры URL.
При запуске приложения в режиме отладки (debug=True), Flask автоматически перезапускает сервер при каждом изменении кода, что упрощает разработку и отладку."""
