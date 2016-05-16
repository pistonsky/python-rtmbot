import os
import pytz
import requests
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.utils import *
from core.total_time_presenter import TotalTimePresenter
from core.actions_presenter import ActionsPresenter


class TrelloBot:

    API_BASE_URL = 'https://api.trello.com/1'
    KEY = None
    TOKEN = None
    BOARD_ID = None
    MEMBER_ID = None
    TIMEZONE = None

    presenter = None
    total_time_presenter = None
    
    def __init__(self, key, token, board_id, member_id, timezone=pytz.utc):
        self.KEY = key
        self.TOKEN = token
        self.BOARD_ID = board_id
        self.MEMBER_ID = member_id
        self.TIMEZONE = timezone
        self.presenter = ActionsPresenter(timezone)
        self.total_time_presenter = TotalTimePresenter(timezone)

    def fetch_my_actions(self, start_period, end_period):
        params = {
            'limit': 1000,
            'memberCreator': 'false',
            'member_fields': 'fullName',
            'since': start_period,
            'before': end_period,
            'fields': 'type,date,data',
            'filter': 'addMemberToCard,removeMemberFromCard',
            'key': self.KEY,
            'token': self.TOKEN
        }
        actions = requests.get('{url}/boards/{board_id}/actions?{params}'.format(
            url=self.API_BASE_URL,
            params=fast_urlencode(params),
            board_id=self.BOARD_ID)).json()
        # loop thru actions and show only mine
        my_actions = []
        for action in reversed(actions):
            if action['member']['id'] == self.MEMBER_ID:
                my_actions.append(action)
        return self.presenter.present(my_actions)

    def get_total_time_message(self, start_period, end_period):
        params = {
            'limit': 1000,
            'memberCreator': 'false',
            'member_fields': 'fullName',
            'since': start_period,
            'before': end_period,
            'fields': 'type,date,data',
            'filter': 'addMemberToCard,removeMemberFromCard',
            'key': self.KEY,
            'token': self.TOKEN
        }
        actions = requests.get('{url}/boards/{board_id}/actions?{params}'.format(
            url=self.API_BASE_URL,
            params=fast_urlencode(params),
            board_id=self.BOARD_ID)).json()
        # loop thru actions and show only mine
        my_actions = []
        for action in reversed(actions):
            if action['member']['id'] == self.MEMBER_ID:
                my_actions.append(action)
        return self.total_time_presenter.present(my_actions)
