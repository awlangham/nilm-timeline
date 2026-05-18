#!/usr/bin/env python3

import sys
import uvicorn

from main import app


if __name__ == '__main__':
    uvicorn.run('main:app', port=8001, reload=True)
