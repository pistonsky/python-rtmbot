import datetime
import pytz


class Action:
    def __init__(self, action, timezone):
        self.action = action
        self.timezone = timezone

    def __str__(self):
        if self.action['type'] == 'addMemberToCard':
            return('Started {name} at {time}'.format(
                id=self.action['data']['card']['id'],
                name=self.action['data']['card']['name'],
                time=pytz.timezone('utc').localize(datetime.datetime.strptime(self.action['date'][:19], '%Y-%m-%dT%H:%M:%S')).astimezone(pytz.timezone(self.timezone)).strftime('%A %-I:%M %p')))
        if self.action['type'] == 'removeMemberFromCard':
            return('Finished with {name} at {time}'.format(
                id=self.action['data']['card']['id'],
                name=self.action['data']['card']['name'],
                time=pytz.timezone('utc').localize(datetime.datetime.strptime(self.action['date'][:19], '%Y-%m-%dT%H:%M:%S')).astimezone(pytz.timezone(self.timezone)).strftime('%A %-I:%M %p')))

    def __sub__(self, other):
        action_a = self.action
        action_b = other
        duration = datetime.datetime.strptime(action_a['date'][:19], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(action_b['date'][:19], '%Y-%m-%dT%H:%M:%S')
        raw_seconds = duration.seconds + duration.days*24*3600
        if raw_seconds < 0:
            raw_seconds *= -1
        return raw_seconds

    def match(self, another_action):
        return another_action['type'] != self.action['type'] and another_action['data']['card']['id'] == self.action['data']['card']['id']
