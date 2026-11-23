# Тесты для ozon_api.py
# запрос к реальному Ozon не делаем - подменяем requests.post

from unittest.mock import patch, MagicMock
import pytest

import ozon_api


@patch('ozon_api.requests.post')
def test_zapros_k_ozonu(mock_post):
    # проверяем что функция правильно обращается к ozon: тот адрес, те заголовки

    podstavnoy_otvet = MagicMock()
    podstavnoy_otvet.status_code = 200
    podstavnoy_otvet.json.return_value = {'items': []}
    mock_post.return_value = podstavnoy_otvet

    ozon_api.get_stocks('client-999', 'key-999')

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args

    assert args[0] == ozon_api.OZON_URL
    assert kwargs['headers']['Client-Id'] == 'client-999'
    assert kwargs['headers']['Api-Key'] == 'key-999'


@patch('ozon_api.requests.post')
def test_oshibka_pri_nevernyh_klyuchah(mock_post):
    # если ozon вернул не 200 - функция должна упасть с понятной ошибкой, а не молча вернуть мусор

    podstavnoy_otvet = MagicMock()
    podstavnoy_otvet.status_code = 401
    podstavnoy_otvet.text = 'Unauthorized'
    mock_post.return_value = podstavnoy_otvet

    with pytest.raises(Exception):
        ozon_api.get_stocks('client-1', 'neverny-key')


@patch('ozon_api.requests.post')
def test_chtenie_json_ot_ozona(mock_post):
    # проверяем что json от озона правильно читается и остатки по складам суммируются

    podstavnoy_json = {
        'items': [
            {
                'offer_id': 'futbolka-m',
                'stocks': [
                    {'type': 'fbs', 'present': 5, 'reserved': 1},
                    {'type': 'fbo', 'present': 3, 'reserved': 0},
                ]
            },
            {
                'offer_id': 'shtany-l',
                'stocks': [
                    {'type': 'fbs', 'present': 0, 'reserved': 0},
                ]
            }
        ]
    }

    podstavnoy_otvet = MagicMock()
    podstavnoy_otvet.status_code = 200
    podstavnoy_otvet.json.return_value = podstavnoy_json
    mock_post.return_value = podstavnoy_otvet

    rezultat = ozon_api.get_stocks('client-1', 'key-1')

    assert len(rezultat) == 2
    assert rezultat[0] == {'offer_id': 'futbolka-m', 'ostatok': 8}
    assert rezultat[1] == {'offer_id': 'shtany-l', 'ostatok': 0}
