from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import numpy as np
import uvicorn
from importlib.resources import files

from nilmevents import get_connection
import nilmtimeline

app = FastAPI()

event_set = 'tbay_engine_room'
app.event_db = get_connection(event_set)


def get_distance(transient_tPQ, exemplar_tPQ):
    # Remove the timestamp
    exemplar_PQ = exemplar_tPQ[1:]
    transient_PQ = transient_tPQ[1:]

    exemplar_P_ss = np.mean(exemplar_PQ[0, -5:])
    exemplar_Q_ss = np.mean(exemplar_PQ[1, -5:])

    transient_P_ss = np.mean(transient_PQ[0, -5:])
    transient_Q_ss = np.mean(transient_PQ[1, -5:])

    return np.linalg.norm([exemplar_P_ss - transient_P_ss, exemplar_Q_ss - transient_Q_ss]) / np.linalg.norm([exemplar_P_ss, exemplar_Q_ss])


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

    load_data = []
    current_start_times = {}
    current_start_ids = {}
    current_distance = {}
    for result in results:
        label, timestamp, on_off, event_id = result

        if label not in current_start_times:
            current_start_times[label] = None
            current_start_ids[label] = None
            current_distance[label] = on_distance()

        if on_off == 'ON':
            current_start_times[label] = timestamp
            current_start_ids[label] = event_id
            current_distance[label] = on_distance()

        elif on_off == 'OFF':
            if current_start_times[label] is not None:
                load_data.append({'name': label, 'start_ts': current_start_times[label], 'end_ts': timestamp, 'id': current_start_ids[label], 'distance': current_distance[label]})
                current_start_times[label] = None

    # for label in current_start_times:
    #     if current_start_times[label] is not None:
    #         load_data.append({'name': label, 'start_ts': current_start_times[label], 'end_ts': end_ts, 'id': current_start_ids[label], 'distance': current_distance[label]})

    return {
        'loads': load_data
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
        'distance': get_distance(event_transient, exemplar_transient)
    }


# @app.get('/api/exemplar/{label}')
# async def get_exemplar(label: str):
#     exemplar_tPQ = app.event_db.exemplar(label, 'ON')

#     timestamps = exemplar_tPQ[0] / 1e6
#     timestamps -= timestamps[0]
#     P = exemplar_tPQ[1]
#     Q = exemplar_tPQ[2]

#     return {
#         'timestamps': timestamps.tolist(),
#         'P': P.tolist(),
#         'Q': Q.tolist()
#     }

static_path = files(nilmtimeline).joinpath('static')
app.mount('/', StaticFiles(directory=static_path, html=True), name='static')

def run():
    uvicorn.run('nilmtimeline.main:app', port=8001)