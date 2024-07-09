from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
import numpy as np
from joule.api import get_node
import uvicorn
from importlib.resources import files
import click


from merlin.installation import load_exemplar
from merlin.supervised.trainola import trainola

import nilmtimeline
from nilmtimeline.interval import find_intervals
from nilmtimeline.transient import Transient

from nilmtimeline.endpoints import range, data

app = FastAPI()

app.include_router(range.router)
app.include_router(data.router)


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


@click.command()
@click.argument('dataset')
def run(dataset: str):
    app.dataset = dataset
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=8050)
