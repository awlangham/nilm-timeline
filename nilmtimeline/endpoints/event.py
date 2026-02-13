import json
import numpy as np
from fastapi import APIRouter, Request
from joule.api import get_node

from merlin.api import get_installation
from merlin.utilities import trainola

from nilmtimeline.transient import SinglePhaseTransient, ThreePhaseTransient
# from nilmtimeline.interval import find_intervals

router = APIRouter()


@router.get('/api/event/{start_ts}/{end_ts}')
async def get_event(start_ts: int, end_ts: int, request: Request):
    node = get_node()

    # Get label
    events = await node.event_stream_read_list(request.app.dataset + '/events', start=start_ts, end=start_ts + 1)
    event_label = events[0].content['label']

    current_installation = get_installation()
    if current_installation.num_phases == 3:
        TransientClass = ThreePhaseTransient
    else:
        TransientClass = SinglePhaseTransient

    # Get ON transient
    on_selected_data = await current_installation.get_transient(start_ts, start_ts + 1e6)
    on_transient = TransientClass(on_selected_data)

    # Get OFF transient
    off_selected_data = await current_installation.get_transient(end_ts - 1e6, end_ts)
    off_transient = TransientClass(off_selected_data, is_on=False)

    # Get ON exemplar
    on_exemplar_data = await current_installation.get_exemplar(event_label, 'OFF', 'ON')
    on_exemplar = TransientClass(on_exemplar_data)

    # Get OFF exemplar
    off_exemplar_data = await current_installation.get_exemplar(event_label, 'ON', 'OFF')
    off_exemplar = TransientClass(off_exemplar_data, is_on=False)

    json_filter = json.dumps([[['label', 'is', event_label]]])
    last_24h_events = await node.event_stream_read_list(request.app.dataset + '/events', start=start_ts - 24 * 60 * 60e6, end=start_ts, json_filter=json_filter)

    event = (await node.event_stream_read_list(request.app.dataset + '/events', start=start_ts, end=start_ts + 1))[0]

    await node.close()

    last_24h_ons = [event for event in last_24h_events if event.content['type'] == 'OFF to ON']
    # run_durations = [interval['end_ts'] - interval['start_ts'] for interval in find_intervals(last_24h_events, event_label)]

    cf = current_installation.read_config()
    on_ss = cf['loads'][event_label]['states']['ON']

    if current_installation.num_phases == 3:
        P_ss_nom = on_ss[0] + on_ss[2] + on_ss[4]
        Q_ss_nom = on_ss[1] + on_ss[3] + on_ss[5]
    else:
        P_ss_nom = on_ss[0]
        Q_ss_nom = on_ss[1]

    metrics = {
        'P_ss_nom': P_ss_nom,
        'Q_ss_nom': Q_ss_nom,
        'P_ss_seen': event.content['P_ss'],
        'Q_ss_seen': event.content['Q_ss'],
        'num_runs_24h': len(last_24h_ons),
        # 'avg_run_duration': np.mean(run_durations) / 1e6 if len(run_durations) > 0 else None,
        'on_distance': trainola(on_selected_data.T[1:], on_exemplar_data.T[1:]),
        'off_distance': trainola(off_selected_data.T[1:], off_exemplar_data.T[1:]),
        'zero_seen': [np.real(on_transient.zero_signature), np.imag(on_transient.zero_signature)],
        'zero_nom': [np.real(on_exemplar.zero_signature), np.imag(on_exemplar.zero_signature)]
    }

    return {
        'on_transient': on_transient.to_dict(),
        'off_transient': off_transient.to_dict(),
        'on_exemplar': on_exemplar.to_dict(),
        'off_exemplar': off_exemplar.to_dict(),
        'load_name': event_label,
        'metrics': metrics
    }
