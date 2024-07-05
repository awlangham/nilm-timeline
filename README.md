NILM Timeline
========

Load schedule timeline with transient-based distance metric visualization.

Development
------------

Install NILM Timeline for development by cloning this repository and opening it in a terminal. Then run

    pip -m venv venv
    source venv/bin/activate
    pip install -e .

This creates a new Python virtual environment and installs nilm-timeline in editable mode, so that changes to the source code are immediately reflected in the virtual environment's installation.

To run the development version of the visualization back-end, open a terminal in nilm-timeline/nilmtimeline and run ``./start_dev.py <dataset_name>``.
For the visualization front-end, open a terminal in nilm-timeline/frontend and run ``./start_dev.sh``. Note that [Node.js](https://nodejs.org) must be installed for front-end development.
