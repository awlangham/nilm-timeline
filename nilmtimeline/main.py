from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from importlib.resources import files
import click
from pathlib import Path
from merlin.api import get_installation
import json

import nilmtimeline
from nilmtimeline.endpoints import range, data, event

app = FastAPI()

app.include_router(range.router)
app.include_router(data.router)
app.include_router(event.router)

default_path = Path('/opt/configs')
config_filename = str(default_path / 'nilmtimeline.json') if default_path.exists() else str(files(nilmtimeline) / 'nilmtimeline.json')

with open(config_filename, 'r') as nilm_timeline_config:
    cf = json.load(nilm_timeline_config)
    merlin_config = get_installation().read_config()
    app.dataset = merlin_config['stream_name']
    app.voltage = cf['voltage']
    app.sequence = cf['sequence']
    app.thresholds = cf['thresholds']

@click.command()
def run():
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=8051)
