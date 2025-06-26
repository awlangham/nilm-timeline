import numpy as np


class Transient:
    def __init__(self, data, is_on=True) -> None:
        self.timestamps = data[:, 0] - data[0, 0]
        self.timestamps = self.timestamps / 1e6

        self.P = data[:, 1] + data[:, 9] + data[:, 17]
        self.Q = data[:, 2] + data[:, 10] + data[:, 18]

        if is_on:
            self.P -= np.mean(self.P[:5])
            self.Q -= np.mean(self.Q[:5])
        else:
            self.P -= np.mean(self.P[-5:])
            self.Q -= np.mean(self.Q[-5:])

    def to_dict(self) -> str:
        return {'timestamps': self.timestamps.tolist(), 'P': self.P.tolist(), 'Q': self.Q.tolist()}
