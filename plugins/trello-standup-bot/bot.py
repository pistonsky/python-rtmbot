from datetime import date, datetime, timedelta
from lib.trello_bot import TrelloBot
from config.settings import *


crontable = []
outputs = []


def process_message(data):

    text = data['text'].lower()

    if 'was doing yesterday' in text and 'what' in text:
        for name in MEMBER_IDS:
            if name in data['text']:
                # for the previous workday - if today is monday, show actions since friday
                weekday = date.today().weekday()
                if (weekday == 0):  # Monday
                    start_period = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d')
                elif (weekday == 6):  # Sunday
                    start_period = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
                else:  # Saturday and any other days
                    start_period = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
                end_period = date.today().strftime('%Y-%m-%d')
                bot = TrelloBot(KEY, TOKEN, BOARD_ID, MEMBER_IDS[name], TIMEZONE)
                message = bot.fetch_my_actions(start_period, end_period)
                outputs.append([data['channel'], '{} was quite busy. Specifically:\n\n{}'.format(name, '\n'.join(list(map(lambda x: '>' + x, message.split('\n')))))])

    if 'totals' in text:
        if 'yesterday' in text:
            message = ''
            # for the previous workday - if today is monday, show actions since friday
            weekday = date.today().weekday()
            if (weekday == 0):  # Monday
                start_period = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d')
            elif (weekday == 6):  # Sunday
                start_period = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
            else:  # Saturday and any other days
                start_period = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            end_period = date.today().strftime('%Y-%m-%d')
            for man in MEMBER_IDS:
                bot = TrelloBot(KEY, TOKEN, BOARD_ID, MEMBER_IDS[man], TIMEZONE)
                message += '{}: {}'.format(man, bot.get_total_time_message(start_period, end_period))
            outputs.append([data['channel'], 'The team was quite busy yesterday:\n\n{}'.format('\n'.join(list(map(lambda x: '>' + x, message.split('\n')))))])
        if 'last week' in text:
            message = ''
            weekday = date.today().weekday()
            start_period = (date.today() - timedelta(days=weekday+7)).strftime('%Y-%m-%d')
            end_period = (date.today() - timedelta(days=weekday)).strftime('%Y-%m-%d')
            for man in MEMBER_IDS:
                bot = TrelloBot(KEY, TOKEN, BOARD_ID, MEMBER_IDS[man], TIMEZONE)
                message += '{}: {}'.format(man, bot.get_total_time_message(start_period, end_period))
            outputs.append([data['channel'], 'The team was quite busy last week:\n\n{}'.format('\n'.join(list(map(lambda x: '>' + x, message.split('\n')))))])

