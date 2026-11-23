# Тест для bot.py - проверяем что бот отправляет пользователю правильные сообщения
# в реальный телеграм и в реальный ozon не стучимся - все подменяем

import os
import bot


class FakeChat:
    def __init__(self, chat_id):
        self.id = chat_id


class FakeMessage:
    # упрощенная замена message от телеграма, нам нужны только chat.id и text
    def __init__(self, chat_id, text):
        self.chat = FakeChat(chat_id)
        self.text = text


def test_otpravka_privetstviya(monkeypatch):
    # проверяем что на /start бот шлет пользователю приветствие с просьбой прислать api-key

    otpravlennye_soobscheniya = []

    monkeypatch.setattr(bot.bot, 'send_message', lambda chat_id, text: otpravlennye_soobscheniya.append((chat_id, text)))
    monkeypatch.setattr(bot.db, 'log_action', lambda *args, **kwargs: None)

    bot.start(FakeMessage(111, '/start'))

    assert len(otpravlennye_soobscheniya) == 1
    chat_id, text = otpravlennye_soobscheniya[0]
    assert chat_id == 111
    assert 'Api-Key' in text


def test_otpravka_otcheta(tmp_path, monkeypatch):
    # проверяем что команда /report шлет пользователю и картинку, и csv файл

    monkeypatch.chdir(tmp_path)
    os.mkdir('data')

    otpravlennye_soobscheniya = []
    otpravlennye_foto = []
    otpravlennye_dokumenty = []

    monkeypatch.setattr(bot.bot, 'send_message', lambda chat_id, text: otpravlennye_soobscheniya.append(text))
    monkeypatch.setattr(bot.bot, 'send_photo', lambda chat_id, photo, caption=None: otpravlennye_foto.append(chat_id))
    monkeypatch.setattr(bot.bot, 'send_document', lambda chat_id, doc: otpravlennye_dokumenty.append(chat_id))

    monkeypatch.setattr(bot.db, 'get_client', lambda chat_id: ('client-1', 'key-1'))
    monkeypatch.setattr(bot.db, 'log_action', lambda *args, **kwargs: None)
    monkeypatch.setattr(bot.ozon_api, 'get_stocks', lambda client_id, api_key: [{'offer_id': 'tovar-1', 'ostatok': 5}])

    bot.report_command(FakeMessage(222, '/report'))

    assert len(otpravlennye_foto) == 1
    assert len(otpravlennye_dokumenty) == 1
    assert otpravlennye_foto[0] == 222


def test_otpravka_bez_klyuchey(monkeypatch):
    # если пользователь еще не вводил ключи - бот должен попросить его сделать /start,
    # а не пытаться лезть в ozon api

    otpravlennye_soobscheniya = []

    monkeypatch.setattr(bot.bot, 'send_message', lambda chat_id, text: otpravlennye_soobscheniya.append(text))
    monkeypatch.setattr(bot.db, 'get_client', lambda chat_id: None)

    bot.report_command(FakeMessage(333, '/report'))

    assert len(otpravlennye_soobscheniya) == 1
    assert '/start' in otpravlennye_soobscheniya[0]
