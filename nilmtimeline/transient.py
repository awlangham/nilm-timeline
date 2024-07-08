import numpy as np


class Transient:
    def __init__(self, data, is_on=True) -> None:
        self.timestamps = data[:, 0] - data[0, 0]
        self.timestamps = self.timestamps / 1e6

        if is_on:
            self.P = data[:, 1] - np.mean(data[:5, 1])
            self.Q = data[:, 2] - np.mean(data[:5, 2])
        else:
            self.P = data[:, 1] - np.mean(data[-5:, 1])
            self.Q = data[:, 2] - np.mean(data[-5:, 2])

    def to_dict(self) -> str:
        return {'timestamps': self.timestamps.tolist(), 'P': self.P.tolist(), 'Q': self.Q.tolist()}
