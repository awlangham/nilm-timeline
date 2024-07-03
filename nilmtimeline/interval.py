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
            'distance': self.distance, # TODO
            'num_on': 1,  # TODO
            'max_on': 1  # TODO
        }
