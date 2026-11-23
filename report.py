# Модуль для формирования отчета - картинка с графиком и csv файл с данными

import csv
import matplotlib.pyplot as plt


def make_chart(spisok_ostatkov, chat_id):
    # строим простой столбчатый график по остаткам товаров
    # если товаров много - берем только первые 15, чтобы график влез и был читаемым

    top_tovary = spisok_ostatkov[:15]

    nazvaniya = [t['offer_id'] for t in top_tovary]
    ostatki = [t['ostatok'] for t in top_tovary]

    plt.figure(figsize=(10, 6))
    plt.bar(nazvaniya, ostatki)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Товар')
    plt.ylabel('Остаток, шт')
    plt.title('Остатки товаров на складах Ozon')
    plt.tight_layout()

    put_k_faylu = f'data/chart_{chat_id}.png'
    plt.savefig(put_k_faylu)
    plt.close()

    return put_k_faylu


def save_csv(spisok_ostatkov, chat_id):
    # сохраняем полный список остатков в csv файл
    put_k_faylu = f'data/stocks_{chat_id}.csv'

    with open(put_k_faylu, 'w', newline='', encoding='utf-8-sig') as f:
        pisatel = csv.writer(f)
        pisatel.writerow(['offer_id', 'ostatok'])

        for tovar in spisok_ostatkov:
            pisatel.writerow([tovar['offer_id'], tovar['ostatok']])

    return put_k_faylu
