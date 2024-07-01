from fastapi import FastAPI
import json
import numpy as np
from joule.api import get_node

from merlin.installation import load_exemplar
from merlin.supervised.trainola import trainola

from nilmtimeline.interval import Interval
from nilmtimeline.find_intervals import find_intervals

app = FastAPI()


@app.get('/api/range')
async def get_range():
    node = get_node()
    event_info = await node.event_stream_info(app.dataset + '/events')
    await node.close()

    return {
        'range_start': event_info.end - 24 * 60 * 60e6,
        'range_end': event_info.end
    }


@app.get('/api/data')
async def get_data(start_ts: int, end_ts: int):
    node = get_node()
    events = await node.event_stream_read(app.dataset + '/events', start=start_ts, end=end_ts)
    await node.close()

    start_times = {}
    intervals = []
    load_names = set()
    for event in events:
        try:
            load_name = event.content['label']
            load_names.add(load_name)
        except KeyError:
            continue

        if event.content['type'] == 'OFF to ON':
            start_times[load_name] = event.start_time
        elif event.content['type'] == 'ON to OFF':
            try:
                start_time = start_times[load_name]
            except:
                continue

            interval = Interval(load_name, start_time, event.end_time)
            intervals.append(interval.to_dict())
            del start_times[load_name]

    return {
        'loads': intervals,
        'labels': list(load_names)
    }


@app.get('/api/event/{timestamp}')
async def get_event(timestamp: int):
    node = get_node()
    data = await node.data_read_array(app.dataset + '/transients', flatten=True, start=timestamp, end=timestamp + 1e6)

    event_timestamps = data[:, 0] - data[0, 0]
    event_timestamps = event_timestamps / 1e6
    event_P = data[:, 1] - np.mean(data[:5, 1])
    event_Q = data[:, 2] - np.mean(data[:5, 2])

    events = await node.event_stream_read(app.dataset + '/events', start=timestamp, end=timestamp + 1)
    event_label = events[0].content['label']

    off_on_exemplar = await load_exemplar(event_label, 'OFF', 'ON')
    exemplar_timestamps = off_on_exemplar[:, 0] - off_on_exemplar[0, 0]
    exemplar_timestamps = exemplar_timestamps / 1e6
    exemplar_P = off_on_exemplar[:, 1] - np.mean(off_on_exemplar[:5, 1])
    exemplar_Q = off_on_exemplar[:, 2] - np.mean(off_on_exemplar[:5, 2])

    json_filter = json.dumps([[['label', 'is', event_label]]])
    last_24h_events = await node.event_stream_read(app.dataset + '/events', start=timestamp - 24 * 60 * 60e6, end=timestamp, json_filter=json_filter)

    await node.close()

    last_24h_ons = [event for event in last_24h_events if event.content['type'] == 'OFF to ON']
    run_durations = [interval['end_ts'] - interval['start_ts'] for interval in find_intervals(last_24h_events)]

    metrics = {
        'num_runs_24h': len(last_24h_ons),
        'avg_run_duration': np.mean(run_durations) / 1e6,
        'distance_from_exemplar': trainola(data.T, off_on_exemplar.T)
    }

    return {
        'transient': {'timestamps': event_timestamps.tolist(), 'P': event_P.tolist(), 'Q': event_Q.tolist()},
        'exemplar': {'timestamps': exemplar_timestamps.tolist(), 'P': exemplar_P.tolist(), 'Q': exemplar_Q.tolist()},
        'metrics': metrics
    }
