from nilmtimeline.interval import Interval


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

    return intervals
