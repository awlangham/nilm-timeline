from fastapi import APIRouter, Request
from joule.api import get_node

from merlin.installation import CurrentInstallation
from nilmtimeline.interval import find_intervals

router = APIRouter()


@router.get('/api/data')
async def get_data(start_ts: int, end_ts: int, request: Request):
    node = get_node()
    installation = CurrentInstallation(node)
    load_names = installation.get_load_names()

    intervals = []
    for load_name in load_names:
        events = await node.event_stream_read(
            request.app.dataset + '/events',
            start=start_ts,
            end=end_ts
        )

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

        intervals += find_intervals(load_events, load_name)

    await node.close()

    return {
        'loads': intervals,
        'labels': load_names
    }
