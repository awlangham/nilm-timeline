from nilmtimeline.interval import Interval


def find_intervals(events):
    start_time = None
    intervals = []
    for event in events:
        if event.content['type'] == 'OFF to ON':
            start_time = event.start_time
        elif event.content['type'] == 'ON to OFF' and start_time is not None:
            interval = Interval(None, start_time, event.end_time)
            intervals.append(interval.to_dict())
            start_time = None

    return intervals
