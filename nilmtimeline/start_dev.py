#!/usr/bin/env python3

import sys
import uvicorn

from main import app

app.dataset = sys.argv[1]
app.threshold = float(sys.argv[2])
app.voltage = float(sys.argv[3])
app.sequence = sys.argv[4]

if __name__ == '__main__':
    uvicorn.run('main:app', port=8001, reload=True)
