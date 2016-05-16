class Card:
    def __init__(self, duration, data):
        self.duration = duration
        self.name = data['name']
        self.data = data

    def for_human(self, raw_seconds):
        if raw_seconds < 60:
            result = '{} seconds'.format(raw_seconds)
        else:
            seconds = raw_seconds % 60
            minutes = (raw_seconds - seconds) / 60
            if minutes == 1:
                result = '1 minute'
            elif minutes < 60:
                result = '{0:.0f} minutes'.format(minutes)
            else:
                hours = minutes // 60
                minutes = minutes % 60
                if hours == 1:
                    if minutes < 2:
                        result = '1 hour'
                    else:
                        result = '1 hour {0:.0f} minutes'.format(minutes)
                elif hours < 4:
                    if minutes < 2:
                        result = '{0:.0f} hours'.format(hours)
                    else:
                        result = '{0:.0f} hours {0:.0f} minutes'.format(hours, minutes)
                else:
                    if minutes < 15:
                        result = '{0:.0f} hours'.format(hours)
                    elif minutes < 45:
                        result = '{0:.0f} and a half hours'.format(hours)
                    else:
                        result = '{0:.0f} hours'.format(hours+1)
        return result


    def __str__(self):
        if self.duration < 7200:
            return '[{duration}] {card}'.format(card=self.name, duration=self.for_human(self.duration))
        else:
            return '[{duration}] {card}'.format(card=self.name, duration=self.for_human(self.duration))
