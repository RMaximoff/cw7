import requests
from django.conf import settings


def tg_get_updates(offset=None):
    params = {}
    if offset is not None:
        params = {'offset': offset}
    response = requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates', params=params)
    return response.json()


def tg_send_message(chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)