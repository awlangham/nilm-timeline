import numpy as np
from joule.utilities import time_now


def find_intervals(events, load_name):
    start_time = None
    faulty = None
    intervals = []
    for event in events:
        if event.content['type'] == 'OFF to ON':
            start_time = event.start_time
            # TODO: use both OFF and ON distances
            # distance = event.content['distance']
            faulty = np.sqrt(event.content['I0_i'] ** 2 + event.content['I0_q'] ** 2) > 0.01 # TO DO parametrize this and remove exemplar offset
        elif event.content['type'] == 'ON to OFF' and start_time is not None:
            interval = Interval(load_name, start_time, event.end_time, faulty)
            intervals.append(interval.to_dict())
            start_time = None
            faulty = None

    # If the last event is an ON, return it too
    if start_time is not None:
        interval = Interval(load_name, start_time, time_now(), faulty)
        intervals.append(interval.to_dict())

    return intervals


class Interval:
    def __init__(self, load_name, start, end, faulty) -> None:
        self.load_name = load_name
        self.start = start
        self.end = end
        self.faulty = faulty

    def to_dict(self):
        return {
            'name': self.load_name,
            'start_ts': self.start,
            'end_ts': self.end,
            'faulty': bool(self.faulty),
            'num_on': 1,  # TODO
            'max_on': 1  # TODO
        }
