import numpy as np
import asyncio
import click
import matplotlib.pyplot as plt
from joule.api import get_node
from joule.utilities import human_to_timestamp as h2ts


@click.command()
@click.argument('stream')
@click.option('-s', '--start_time', required=True)
@click.option('-e', '--end_time', required=True)
def run(stream: str, start_time: str, end_time: str):
    prep_data = asyncio.run(_get_prep_data(stream, h2ts(start_time), h2ts(end_time)))
    timestamps = prep_data[:, 0]
    timestamps -= timestamps[0]
    timestamps = timestamps / 1e6

    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True, tight_layout=True)
    fig.suptitle('abc')
    (I0, I_plus, I_minus) = compute_sequence(prep_data, 'abc')
    ax[0].plot(timestamps, np.real(I0))
    ax[0].plot(timestamps, np.imag(I0))
    ax[0].set_title('Zero sequence')
    ax[0].set_xlim(timestamps[0], timestamps[-1])

    ax[1].plot(timestamps, np.real(I_plus))
    ax[1].plot(timestamps, np.imag(I_plus))
    ax[1].set_title('Positive sequence')

    ax[2].plot(timestamps, np.real(I_minus))
    ax[2].plot(timestamps, np.imag(I_minus))
    ax[2].set_title('Negative sequence')

    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True, tight_layout=True)
    fig.suptitle('acb')
    (I0, I_plus, I_minus) = compute_sequence(prep_data, 'acb')
    ax[0].plot(timestamps, np.real(I0))
    ax[0].plot(timestamps, np.imag(I0))
    ax[0].set_title('Zero sequence')
    ax[0].set_xlim(timestamps[0], timestamps[-1])

    ax[1].plot(timestamps, np.real(I_plus))
    ax[1].plot(timestamps, np.imag(I_plus))
    ax[1].set_title('Positive sequence')

    ax[2].plot(timestamps, np.real(I_minus))
    ax[2].plot(timestamps, np.imag(I_minus))
    ax[2].set_title('Negative sequence')

    plt.show()


def compute_sequence(prep_data, sequence):
    PA, QA, PB, QB, PC, QC = prep_data[:, (1, 2, 9, 10, 17, 18)].T
    alpha = np.exp(2 * np.pi * 1j / 3)
    A_inverse = np.ones((3, 3), dtype=complex)

    if sequence == 'acb':
        alpha = 1 / alpha

    A_inverse[1, 1] = alpha
    A_inverse[2, 2] = alpha
    A_inverse[1, 2] = alpha ** 2
    A_inverse[2, 1] = alpha ** 2

    IA = (PA - QA * 1j)
    IB = (PB - QB * 1j) / alpha
    IC = (PC - QC * 1j) / (alpha ** 2)

    I_phase = np.array([IA, IB, IC])
    I_sequence = (A_inverse @ I_phase).T / 3
    return I_sequence.T


async def _get_prep_data(stream_name: str, start: int, end: int):
    node = get_node()
    pipe = await node.data_read(stream_name, start=start, end=end)
    data = await pipe.read_all(flatten=True)
    await node.close()
    return data
