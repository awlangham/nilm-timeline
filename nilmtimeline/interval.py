from joule.utilities import time_now


def find_intervals(events, load_name):
    start_time = None
    distance = None
    intervals = []
    for event in events:
        if event.content['type'] == 'OFF to ON':
            start_time = event.start_time
            # TODO: use both OFF and ON distances
            distance = event.content['distance']
        elif event.content['type'] == 'ON to OFF' and start_time is not None:
            interval = Interval(load_name, start_time, event.end_time, distance)
            intervals.append(interval.to_dict())
            start_time = None

    # If the last event is an ON, return it too
    if start_time is not None and distance is not None:
        interval = Interval(load_name, start_time, time_now(), distance)
        intervals.append(interval.to_dict())

    return intervals


class Interval:
    def __init__(self, load_name, start, end, distance) -> None:
        self.load_name = load_name
        self.start = start
        self.end = end
        self.distance = distance

    def to_dict(self):
        return {
            'name': self.load_name,
            'start_ts': self.start,
            'end_ts': self.end,
            'distance': self.distance,
            'num_on': 1,  # TODO
            'max_on': 1  # TODO
        }
