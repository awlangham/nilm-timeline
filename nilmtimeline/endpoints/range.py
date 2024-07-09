from fastapi import APIRouter, Request

from joule.api import get_node

router = APIRouter()


@router.get('/api/range')
async def get_range(request: Request):
    node = get_node()
    event_info = await node.event_stream_info(request.app.dataset + '/events')
    await node.close()

    return {
        'range_start': event_info.end - 1 * 60 * 60e6,  # 1 hour
        'range_end': event_info.end
    }
