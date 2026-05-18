from pathlib import Path
from importlib.resources import files

import nilmtimeline

default_path = Path('/opt/configs')
config_filename = str(default_path / 'nilmtimeline.json') if default_path.exists() else str(files(nilmtimeline) / 'nilmtimeline.json')
