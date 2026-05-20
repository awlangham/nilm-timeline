import numpy as np
from joule.utilities import time_now


def compute_zs_current(event, v_rms, sequence):
    alpha = np.exp(2 * np.pi * 1j / 3)
    A_inverse = np.ones((3, 3), dtype=complex)

    if sequence == 'acb':
        alpha = 1 / alpha

    A_inverse[1, 1] = alpha
    A_inverse[2, 2] = alpha
    A_inverse[1, 2] = alpha ** 2
    A_inverse[2, 1] = alpha ** 2

    PA_ss = event.content['PA_ss']
    QA_ss = event.content['QA_ss']

    PB_ss = event.content['PB_ss']
    QB_ss = event.content['QB_ss']

    PC_ss = event.content['PC_ss']
    QC_ss = event.content['QC_ss']

    IA = (PA_ss - QA_ss * 1j) / v_rms
    IB = (PB_ss - QB_ss * 1j) / (v_rms * alpha)
    IC = (PC_ss - QC_ss * 1j) / (v_rms * alpha ** 2)

    I_phase = np.array([IA, IB, IC])
    I_sequence = (A_inverse @ I_phase).T / 3

    I0_i, I0_q = np.real(I_sequence[0]), np.imag(I_sequence[0])
    return (I0_i, I0_q)


def check_zero_sequence(seen_event, exemplar_event, threshold, v_rms, sequence):
    I0_i_seen, I0_q_seen = compute_zs_current(seen_event, v_rms, sequence)
    I0_i_exemplar, I0_q_exemplar = compute_zs_current(exemplar_event, v_rms, sequence)

    faulty = np.sqrt((I0_i_seen - I0_i_exemplar) ** 2 + (I0_q_seen - I0_q_exemplar) ** 2) > threshold
    return faulty


def find_intervals(events, load_name, on_exemplar_event, request):
    start_time = None
    faulty = None
    load_threshold = request.app.loads[load_name]['threshold']
    intervals = []
    for event in events:
        if event.content['type'] == 'OFF to ON':
            start_time = event.start_time
            if request.app.i0 and load_threshold is not None:
                v_rms = request.app.voltage
                sequence = request.app.sequence
                faulty = check_zero_sequence(event, on_exemplar_event, load_threshold, v_rms, sequence)
            else:
                faulty = None

        elif event.content['type'] == 'ON to OFF' and start_time is not None:
            interval = Interval(load_name, start_time, event.end_time, faulty)
            intervals.append(interval.to_dict())
            start_time = None
            faulty = None

    # If the last event is an ON, return it too
    if start_time is not None:
        interval = Interval(load_name, start_time, time_now() + 2e6, faulty)
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
