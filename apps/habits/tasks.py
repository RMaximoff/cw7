from datetime import datetime, timedelta
import requests
from celery import shared_task
from django.conf import settings
from apps.habits.models import Habit
from apps.users.models import User

bot_token = settings.TELEGRAM_KEY


@shared_task
def get_tg_chat_id():
    users = User.objects.filter(chat_id=None)
    response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates')
    chats = response.json()['result']
    for user in users:
        for chat in chats:
            if user.telegram == chat['message']['from']['username']:
                user.chat_id = chat['message']['chat']['id']
                user.save()


@shared_task
def send_tg_message():
    time_now = datetime.now()
    habits = Habit.objects.filter(time__gte=time_now - timedelta(minutes=1)).filter(time__lte=time_now)

    for habit in habits:
        message = f'{habit.user.telegram}, it is time to {habit.action} in/at {habit.place}'
        response = requests.get(
            f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={habit.user.chat_id}&text={message}')
        habit.time += timedelta(days=habit.period)
        habit.save()
        return response.json()
