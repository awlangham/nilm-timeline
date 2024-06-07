class Interval:
    def __init__(self, load_name, start, end) -> None:
        self.load_name = load_name
        self.start = start
        self.end = end

    def to_dict(self):
        return {
            'name': self.load_name,
            'start_ts': self.start,
            'end_ts': self.end,
            'num_on': 1,
            'max_on': 1
        }