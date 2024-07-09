import json
from fastapi import APIRouter, Request
from joule.api import get_node

from merlin.installation import CurrentInstallation
from nilmtimeline.interval import find_intervals

router = APIRouter()


@router.get('/api/data')
async def get_data(start_ts: int, end_ts: int, request: Request):
    node = get_node()
    installation = CurrentInstallation()
    load_names = installation.get_load_names()

    intervals = []
    for load_name in load_names:
        json_filter = json.dumps([[['label', 'is', load_name]]])
        load_events = await node.event_stream_read(
            request.app.dataset + '/events',
            start=start_ts,
            end=end_ts,
            json_filter=json_filter
        )
        intervals += find_intervals(load_events, load_name)

    await node.close()

    return {
        'loads': intervals,
        'labels': load_names
    }
