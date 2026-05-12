from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from importlib.resources import files
import click

import nilmtimeline
from nilmtimeline.endpoints import range, data, event

app = FastAPI()

app.include_router(range.router)
app.include_router(data.router)
app.include_router(event.router)


@click.command()
@click.argument('dataset')
@click.argument('threshold', type=float)
@click.argument('voltage', type=float)
@click.argument('sequence', type=click.Choice(['abc', 'acb']))
def run(dataset: str, threshold: float, voltage: float, sequence: str):
    app.dataset = dataset
    app.threshold = threshold
    app.voltage = voltage
    app.sequence = sequence
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=8051)
