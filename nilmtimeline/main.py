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
def run(dataset: str):
    app.dataset = dataset
    static_path = files(nilmtimeline).joinpath('static')
    app.mount('/', StaticFiles(directory=static_path, html=True), name='static')
    uvicorn.run('nilmtimeline.main:app', host='', port=8050)
