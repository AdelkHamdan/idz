# Модуль для работы с базой данных
# база простая - sqlite, два стола: клиенты и действия

import sqlite3

DB_FILE = 'data/baza.db'


def podklyuchitsya():
    # открываем соединение с базой (файл создастся сам при первом запуске)
    soedinenie = sqlite3.connect(DB_FILE)
    return soedinenie


def init_db():
    # создаем таблицы если их еще нет
    soedinenie = podklyuchitsya()
    kursor = soedinenie.cursor()

    kursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            client_id TEXT,
            api_key TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    kursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            action TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    soedinenie.commit()
    soedinenie.close()


def save_client(telegram_id, client_id, api_key):
    # сохраняем ключи пользователя (перезаписываем, если он уже вводил раньше)
    soedinenie = podklyuchitsya()
    kursor = soedinenie.cursor()

    kursor.execute('DELETE FROM clients WHERE telegram_id = ?', (telegram_id,))
    kursor.execute(
        'INSERT INTO clients (telegram_id, client_id, api_key) VALUES (?, ?, ?)',
        (telegram_id, client_id, api_key)
    )

    soedinenie.commit()
    soedinenie.close()


def get_client(telegram_id):
    # достаем ключи пользователя по его telegram id
    soedinenie = podklyuchitsya()
    kursor = soedinenie.cursor()

    kursor.execute('SELECT client_id, api_key FROM clients WHERE telegram_id = ?', (telegram_id,))
    rezultat = kursor.fetchone()

    soedinenie.close()
    return rezultat


def log_action(telegram_id, action):
    # записываем действие пользователя (для истории)
    soedinenie = podklyuchitsya()
    kursor = soedinenie.cursor()

    kursor.execute(
        'INSERT INTO actions (telegram_id, action) VALUES (?, ?)',
        (telegram_id, action)
    )

    soedinenie.commit()
    soedinenie.close()
