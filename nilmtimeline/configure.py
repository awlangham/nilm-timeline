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
        configuration['voltage'] = click.prompt('RMS line-to-neutral voltage', type=float)
        configuration['sequence'] = click.prompt('Sequence', type=click.Choice(['abc', 'acb'], case_sensitive=False)).lower()
        configuration['thresholds'] = {}
        
        click.echo('Enter load threshold information:')
        add_loads = True
        while add_loads:
            load_name = click.prompt('Load name', type=str)
            threshold = click.prompt('I0 threshold', type=float)
            configuration['thresholds'][load_name] = threshold
            add_loads = click.confirm('Continue adding loads?')

    with open(config_filename, 'w') as config_file:
        json.dump(configuration, config_file, indent=4)
    click.echo(f'Saved to {config_filename}')
