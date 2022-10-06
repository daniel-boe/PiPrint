#!/bin/bash

cd ~/PiPrint
source venv/bin/activate
uvicorn api:app

#chmod +x ~/PiPrint/run-server.sh