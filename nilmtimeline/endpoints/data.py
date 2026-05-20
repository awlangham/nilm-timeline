from fastapi import APIRouter, Request
from joule.api import get_node

from merlin.api import get_installation
from nilmtimeline.interval import find_intervals

router = APIRouter()


@router.get('/api/data')
async def get_data(start_ts: int, end_ts: int, request: Request):
    node = get_node()
    installation = get_installation()
    
    load_names = list(request.app.loads.keys())

    events = await node.event_stream_read_list(
        request.app.dataset + '/events',
        start=start_ts,
        end=end_ts
    )

    intervals = []
    for load_name in load_names:
        on_exemplar = await installation.get_exemplar(load_name, 'OFF', 'ON')
        on_exemplar_start_ts, on_exemplar_end_ts = on_exemplar[0, 0], on_exemplar[-1, 0]
        on_exemplar_event = (await node.event_stream_read_list(request.app.dataset + '/events', start=on_exemplar_start_ts, end=on_exemplar_end_ts))[0]

        # off_exemplar = await installation.get_exemplar(load_name, 'ON', 'OFF')
        # off_exemplar_start_ts, off_exemplar_end_ts = off_exemplar[0, 0], off_exemplar[-1, 0]
        # off_exemplar_event = (await node.event_stream_read_list(request.app.dataset + '/events', start=off_exemplar_start_ts, end=off_exemplar_end_ts))[0]

        load_events = []
        for event in events:
            try:
                if load_name in event.content['label']:
                    # Check if combinatoric
                    if ',' in event.content['label']:
                        load_index = event.content['label'].split(',').index(load_name)
                        event_type = event.content['type'].split(',')[load_index]
                        event.content['type'] = event_type

                    load_events.append(event)
            except KeyError:
                pass

        intervals += find_intervals(load_events, load_name, on_exemplar_event, request)

    await node.close()

    return {
        'loads': intervals,
        'labels': load_names
    }
