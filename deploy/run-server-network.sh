#!/bin/bash

cd ~/PiPrint
source venv/bin/activate
uvicorn api:app --host 0.0.0.0
