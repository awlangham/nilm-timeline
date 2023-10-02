from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from importlib.resources import files
import click

from nilmevents import get_connection
from nilmevents.utilities import trainola
import nilmtimeline

app = FastAPI()


def get_distance(transient_tPQ, exemplar_tPQ):
    # Remove the timestamp
    exemplar_PQ = exemplar_tPQ[1:]
    transient_PQ = transient_tPQ[1:]
    return trainola(exemplar_PQ, transient_PQ)


@app.get('/api/range')
async def get_range():
    range_start, range_end = app.event_db.get_range()

    return {
        'range_start': range_start,
        'range_end': range_end
    }


@app.get('/api/data')
async def get_data(start_ts: int, end_ts: int):
    def on_distance():
        # The DB query for this is costly, so only run it if there's some reasonable number of events
        max_num_events = 500
        if len(results) < max_num_events:
            transient_tPQ, exemplar_tPQ = app.event_db.transient_and_exemplar(event_id, 'ON')
            return get_distance(transient_tPQ, exemplar_tPQ)
        else:
            return None

    results = app.event_db.run_intervals(start_ts, end_ts)
    loads = app.event_db.get_loads()

    load_num_on = {l[0]: 0 for l in loads}
    load_max_on = {l[0]: l[1] for l in loads}
    load_current_start_time = {l[0]: None for l in loads}
    load_current_start_id = {l[0]: None for l in loads}
    load_current_distance = {l[0]: None for l in loads}

    load_data = []

    for result in results:
        label, timestamp, on_off, event_id = result

        if on_off == 'ON':
            if 0 < load_num_on[label] < load_max_on[label]:
                load_data.append({'name': label, 'start_ts': load_current_start_time[label], 'end_ts': timestamp, 'id': load_current_start_id[label], 'num_on': load_num_on[label], 'max_on': load_max_on[label], 'distance': load_current_distance[label]})

            load_num_on[label] += 1
            load_current_start_time[label] = timestamp
            load_current_start_id[label] = event_id
            load_current_distance[label] = on_distance()

        elif on_off == 'OFF':
            if load_num_on[label] == 1:
                load_data.append({'name': label, 'start_ts': load_current_start_time[label], 'end_ts': timestamp, 'id': load_current_start_id[label], 'num_on': load_num_on[label], 'max_on': load_max_on[label], 'distance': load_current_distance[label]})
                load_current_start_time[label] = None
                load_num_on[label] -= 1
            if load_num_on[label] > 1:
                load_data.append({'name': label, 'start_ts': load_current_start_time[label], 'end_ts': timestamp, 'id': load_current_start_id[label], 'num_on': load_num_on[label], 'max_on': load_max_on[label], 'distance': load_current_distance[label]})
                load_current_start_time[label] = timestamp
                load_num_on[label] -= 1
            
            load_current_distance[label] = 0

    return {
        'loads': load_data,
        'labels': app.event_db.get_labels()
    }


@app.get('/api/event/{event_id}')
async def get_event(event_id: int):
    event_transient, exemplar_transient = app.event_db.transient_and_exemplar(event_id, 'ON')

    event_timestamps = event_transient[0] / 1e6
    event_timestamps -= event_timestamps[0]
    event_P = event_transient[1]
    event_Q = event_transient[2]

    exemplar_timestamps = exemplar_transient[0] / 1e6
    exemplar_timestamps -= exemplar_timestamps[0]
    exemplar_P = exemplar_transient[1]
    exemplar_Q = exemplar_transient[2]

    return {
        'transient': {'timestamps': event_timestamps.tolist(), 'P': event_P.tolist(), 'Q': event_Q.tolist()},
        'exemplar': {'timestamps': exemplar_timestamps.tolist(), 'P': exemplar_P.tolist(), 'Q': exemplar_Q.tolist()},
        'distance': get_distance(event_transient, exemplar_transient),
        'num_daily_runs': app.event_db.num_daily_runs(event_id, 'ON')
    }


@click.command()
@click.option('-p', 'port', type=int, help='Port number to use', default=8001, show_default=True)
@click.argument('event_set_name')
def run(port, event_set_name):
    """
    Run NILM timeline for EVENT_SET_NAME
    """

    app.event_db = get_connection(event_set_name)
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=port)
