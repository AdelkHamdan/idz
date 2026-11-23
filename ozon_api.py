# Модуль для запросов к Ozon Seller API
# берем отчет по остаткам товаров на складах

import requests

OZON_URL = 'https://api-seller.ozon.ru/v3/product/info/stocks'


def get_stocks(client_id, api_key):
    # делаем запрос к озону, в заголовках передаем ключи клиента
    zagolovki = {
        'Client-Id': client_id,
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    telo_zaprosa = {
        'cursor': '',
        'filter': {'visibility': 'ALL'},
        'limit': 50
    }

    otvet = requests.post(OZON_URL, headers=zagolovki, json=telo_zaprosa, timeout=15)

    if otvet.status_code != 200:
        # если ключи неверные или еще какая-то ошибка - дальше не идем
        raise Exception(f'Ozon API вернул ошибку, код {otvet.status_code}: {otvet.text}')

    dannye = otvet.json()
    tovary = dannye.get('items', [])

    # собираем простой список: название товара и сколько штук на складах
    spisok_ostatkov = []

    for tovar in tovary:
        nazvanie = tovar.get('offer_id', 'без названия')
        summa_ostatkov = 0

        for sklad in tovar.get('stocks', []):
            summa_ostatkov += sklad.get('present', 0)

        spisok_ostatkov.append({'offer_id': nazvanie, 'ostatok': summa_ostatkov})

    return spisok_ostatkov
