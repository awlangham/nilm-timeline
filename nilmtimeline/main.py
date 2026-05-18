from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from importlib.resources import files
import click
from merlin.api import get_installation
import json

import nilmtimeline
from nilmtimeline.endpoints import range, data, event

app = FastAPI()

app.include_router(range.router)
app.include_router(data.router)
app.include_router(event.router)

with open(nilmtimeline.config_filename, 'r') as nilm_timeline_config:
    cf = json.load(nilm_timeline_config)
    merlin_config = get_installation().read_config()
    app.dataset = merlin_config['stream_name']

    if cf == {}:
        # Blank config, don't enable I0
        app.i0 = False
    else:
        app.i0 = True
        app.voltage = cf['voltage']
        app.sequence = cf['sequence']
        app.thresholds = cf['thresholds']

@click.version_option()
@click.command()
def run():
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=8051)
