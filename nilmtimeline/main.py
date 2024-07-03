from fastapi import FastAPI
import json
import numpy as np
from joule.api import get_node

from merlin.installation import load_exemplar
from merlin.installation import CurrentInstallation
from merlin.supervised.trainola import trainola

from nilmtimeline.find_intervals import find_intervals

app = FastAPI()


@app.get('/api/range')
async def get_range():
    node = get_node()
    event_info = await node.event_stream_info(app.dataset + '/events')
    await node.close()

    return {
        'range_start': event_info.end - 6 * 60 * 60e6,  # 6 hours
        'range_end': event_info.end
    }


@app.get('/api/data')
async def get_data(start_ts: int, end_ts: int):
    node = get_node()
    installation = CurrentInstallation()
    load_names = installation.get_load_names()

    intervals = []
    for load_name in load_names:
        json_filter = json.dumps([[['label', 'is', load_name]]])
        load_events = await node.event_stream_read(app.dataset + '/events', start=start_ts, end=end_ts, json_filter=json_filter)
        intervals += find_intervals(load_events, load_name)

    await node.close()

    return {
        'loads': intervals,
        'labels': load_names
    }


@app.get('/api/event/{start_ts}/{end_ts}')
async def get_event(start_ts: int, end_ts: int):
    node = get_node()

    # Get label
    events = await node.event_stream_read(app.dataset + '/events', start=start_ts, end=start_ts + 1)
    event_label = events[0].content['label']

    # Get ON transient
    on_selected_data = await node.data_read_array(app.dataset + '/transients', flatten=True, start=start_ts, end=start_ts + 1e6)
    on_transient = Transient(on_selected_data)

    # Get OFF transient
    off_selected_data = await node.data_read_array(app.dataset + '/transients', flatten=True, start=end_ts - 1e6, end=end_ts)
    off_transient = Transient(off_selected_data, is_on=False)

    # Get ON exemplar
    on_exemplar_data = await load_exemplar(event_label, 'OFF', 'ON')
    on_exemplar = Transient(on_exemplar_data)

    # Get OFF exemplar
    off_exemplar_data = await load_exemplar(event_label, 'ON', 'OFF')
    off_exemplar = Transient(off_exemplar_data, is_on=False)

    json_filter = json.dumps([[['label', 'is', event_label]]])
    last_24h_events = await node.event_stream_read(app.dataset + '/events', start=start_ts - 24 * 60 * 60e6, end=start_ts, json_filter=json_filter)

    await node.close()

    last_24h_ons = [event for event in last_24h_events if event.content['type'] == 'OFF to ON']
    run_durations = [interval['end_ts'] - interval['start_ts'] for interval in find_intervals(last_24h_events, event_label)]

    metrics = {
        'num_runs_24h': len(last_24h_ons),
        'avg_run_duration': np.mean(run_durations) / 1e6 if len(run_durations) > 0 else None,
        'on_distance': trainola(on_selected_data.T[1:], on_exemplar_data.T[1:]),
        'off_distance': trainola(off_selected_data.T[1:], off_exemplar_data.T[1:])
    }

    return {
        'on_transient': on_transient.to_dict(),
        'off_transient': off_transient.to_dict(),
        'on_exemplar': on_exemplar.to_dict(),
        'off_exemplar': off_exemplar.to_dict(),
        'load_name': event_label,
        'metrics': metrics
    }


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
