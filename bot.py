# Главный файл бота
# сценарий простой:
# 1) /start - бот просит прислать api-ключ, потом client-id
# 2) ключи сохраняются в базу
# 3) по команде /report бот идет в Ozon API, строит график по остаткам и шлет его в чат

import telebot

import config
import db
import ozon_api
import report

bot = telebot.TeleBot(config.BOT_TOKEN)

# тут храним на каком шаге диалога находится пользователь
# ключ - id чата, значение - шаг ('ждем_api_key' / 'ждем_client_id')
sostoyanie_polzovatelya = {}

# тут временно держим уже введенный api-ключ, пока ждем client-id
vremennyi_api_key = {}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    sostoyanie_polzovatelya[chat_id] = 'ждем_api_key'
    db.log_action(chat_id, 'start')

    bot.send_message(chat_id, 'Привет! Я бот для отчетов по Ozon.\n\nПришли мне свой Ozon Api-Key.')


@bot.message_handler(commands=['report'])
def report_command(message):
    chat_id = message.chat.id

    klienta_dannye = db.get_client(chat_id)

    if klienta_dannye is None:
        bot.send_message(chat_id, 'Сначала нужно ввести ключи. Напиши /start')
        return

    client_id, api_key = klienta_dannye

    bot.send_message(chat_id, 'Запрашиваю отчет у Ozon, подожди немного...')
    db.log_action(chat_id, 'report_requested')

    try:
        ostatki = ozon_api.get_stocks(client_id, api_key)
    except Exception as oshibka:
        bot.send_message(chat_id, f'Не получилось получить отчет. Проверь ключи.\nОшибка: {oshibka}')
        return

    if len(ostatki) == 0:
        bot.send_message(chat_id, 'Отчет пустой - товаров с остатками не найдено.')
        return

    put_k_grafiku = report.make_chart(ostatki, chat_id)
    put_k_csv = report.save_csv(ostatki, chat_id)

    with open(put_k_grafiku, 'rb') as foto:
        bot.send_photo(chat_id, foto, caption='Остатки товаров на складах Ozon')

    with open(put_k_csv, 'rb') as fayl:
        bot.send_document(chat_id, fayl)

    db.log_action(chat_id, 'report_sent')


@bot.message_handler(content_types=['text'])
def obrabotat_tekst(message):
    chat_id = message.chat.id
    tekst = message.text.strip()

    shag = sostoyanie_polzovatelya.get(chat_id)

    if shag == 'ждем_api_key':
        vremennyi_api_key[chat_id] = tekst
        sostoyanie_polzovatelya[chat_id] = 'ждем_client_id'
        bot.send_message(chat_id, 'Принято. Теперь пришли свой Client-Id.')

    elif shag == 'ждем_client_id':
        api_key = vremennyi_api_key.get(chat_id)
        client_id = tekst

        db.save_client(chat_id, client_id, api_key)
        db.log_action(chat_id, 'keys_saved')

        sostoyanie_polzovatelya[chat_id] = None
        bot.send_message(chat_id, 'Ключи сохранены! Теперь напиши /report, чтобы получить отчет по остаткам.')

    else:
        bot.send_message(chat_id, 'Не понял. Напиши /start, чтобы начать заново.')


if __name__ == '__main__':
    db.init_db()
    print('Бот запущен')
    bot.infinity_polling()
