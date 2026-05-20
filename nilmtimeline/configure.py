import numpy as np
import click
import json

from nilmtimeline import config_filename


@click.command()
def configure():
    """
    Configure NILM Timeline.

    Set whether the I0 detector runs.
    """

    configuration = {}

    zero_sequence = click.confirm('Use I0 detector?')
    if zero_sequence:
        configuration['zero_sequence'] = True
        configuration['voltage'] = click.prompt('RMS line-to-neutral voltage', type=float)
        configuration['sequence'] = click.prompt('Sequence', type=click.Choice(['abc', 'acb'], case_sensitive=False)).lower()
    else:
        configuration['zero_sequence'] = False
        configuration['voltage'] = None
        configuration['sequence'] = None

    click.echo('Enter loads to display:')
    new_loads = {}
    add_loads = True
    while add_loads:
        load_name = click.prompt('Load name', type=str)
        load_props = {'threshold': None}
        if zero_sequence:
            if click.confirm('Track I0 for this load?'):
                load_props['threshold'] = click.prompt('I0 threshold', type=float)

        new_loads[load_name] = load_props
        add_loads = click.confirm('Continue adding loads?')

    configuration['loads'] = new_loads

    with open(config_filename, 'w') as config_file:
        json.dump(configuration, config_file, indent=4)
    click.echo(f'Saved to {config_filename}. Restart nilm-timeline to take effect.')
