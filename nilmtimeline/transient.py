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

        alpha = np.exp(2 * np.pi * 1j / 3)
        A_inverse = np.ones((3, 3), dtype=complex)

        # TO DO: Make parameters sepcific to installation
        alpha = 1 / alpha
        v_rms = 120

        A_inverse[1, 1] = alpha
        A_inverse[2, 2] = alpha
        A_inverse[1, 2] = alpha ** 2
        A_inverse[2, 1] = alpha ** 2

        PA, QA, PB, QB, PC, QC = data[:, (1, 2, 9, 10, 17, 18)].T
        IA = (PA - QA * 1j) / v_rms
        IB = (PB - QB * 1j) / (v_rms * alpha)
        IC = (PC - QC * 1j) / (v_rms * alpha ** 2)

        I_phase = np.array([IA, IB, IC])
        I_sequence = (A_inverse @ I_phase).T

        I0_i, I0_q = np.real(I_sequence[:, 0]), np.imag(I_sequence[:, 0])

        I0_i_ss = np.mean(I0_i[-5:]) - np.mean(I0_i[:5])
        I0_q_ss = np.mean(I0_q[-5:]) - np.mean(I0_q[:5])

        I0_seen = I0_i_ss + 1j * I0_q_ss
        self.zero_signature = I0_seen / 3

    def to_dict(self) -> str:
        return {'timestamps': self.timestamps.tolist(), 'P': self.P.tolist(), 'Q': self.Q.tolist()}
