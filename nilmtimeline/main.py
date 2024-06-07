from fastapi import FastAPI
from joule.api import get_node

from nilmtimeline.interval import Interval

app = FastAPI()


@app.get('/api/range')
async def get_range():

    node = get_node()
    event_info = await node.event_stream_info(app.dataset + '/events')
    await node.close()

    return {
        'range_start': event_info.start,
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
