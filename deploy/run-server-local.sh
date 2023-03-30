#!/bin/bash

cd ~/PiPrint
source venv/bin/activate
uvicorn api:app
