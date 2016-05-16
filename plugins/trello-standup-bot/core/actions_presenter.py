import datetime

from core.abstract_presenter import AbstractPresenter
from core.time_presenter import TimePresenter
from core.card import Card
from core.action import Action


class ActionsPresenter:
    """Actions need to be grouped by cards"""

    def __init__(self, timezone):
        self.cards = []
        self.incomplete_actions = []
        self.timezone = timezone
        self.time_presenter = TimePresenter()

    def analyze_cards(self, raw_actions):
        cards = []
        incomplete_actions = {}
        for action in raw_actions:
            if len(incomplete_actions) > 0:
                matched = False
                for id in list(incomplete_actions):
                    if incomplete_actions[id].match(action):
                        # it's the same card, calculate duration
                        duration = incomplete_actions[id] - action  # "-" is overloaded in Action class
                        cards.append(Card(duration=duration, data=action['data']['card']))
                        incomplete_actions.pop(id)
                        matched = True
                if not matched:
                    incomplete_actions[action['id']] = Action(action, self.timezone)
            else:
                incomplete_actions[action['id']] = Action(action, self.timezone)
        self.cards = cards
        self.incomplete_actions = incomplete_actions

    def show(self):
        message = ''
        for id in self.incomplete_actions:
            message += '{}\n'.format(self.incomplete_actions[id])
        for card in self.cards:
            message += '{}\n'.format(card)
        return message

    def show_total(self):
        total_duration = 0
        for card in self.cards:
            total_duration += card.duration
        return '\n*TOTAL: {}*'.format(self.time_presenter.present(total_duration))
            
    def present(self, data):
        message = ''
        self.analyze_cards(data)
        message += '{}\n'.format(self.show())
        message += '{}\n'.format(self.show_total())
        return message
