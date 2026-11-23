# Тест для report.py - проверяем обработку данных в график и csv

import os
import report


def test_obrabotka_dannyh(tmp_path, monkeypatch):
    # работаем во временной папке, чтобы не мусорить в настоящей data/
    monkeypatch.chdir(tmp_path)
    os.mkdir('data')

    testovye_dannye = [
        {'offer_id': 'tovar-1', 'ostatok': 10},
        {'offer_id': 'tovar-2', 'ostatok': 25},
    ]

    put_k_grafiku = report.make_chart(testovye_dannye, 777)
    put_k_csv = report.save_csv(testovye_dannye, 777)

    # график и csv должны реально появиться на диске
    assert os.path.exists(put_k_grafiku)
    assert os.path.exists(put_k_csv)

    # проверяем содержимое csv - заголовок плюс две строки с товарами
    with open(put_k_csv, encoding='utf-8-sig') as f:
        stroki = f.readlines()

    assert len(stroki) == 3
    assert 'tovar-1' in stroki[1]
    assert 'tovar-2' in stroki[2]


def test_obrabotka_pustogo_spiska(tmp_path, monkeypatch):
    # если товаров нет - функция все равно не должна падать, просто файл будет пустой
    monkeypatch.chdir(tmp_path)
    os.mkdir('data')

    put_k_csv = report.save_csv([], 778)

    with open(put_k_csv, encoding='utf-8-sig') as f:
        stroki = f.readlines()

    assert len(stroki) == 1
