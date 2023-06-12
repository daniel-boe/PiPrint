#!/bin/bash

port=8000;

while getopts p: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
    esac

done

echo "using port: $port";
cd ~/PiPrint
source venv/bin/activate
uvicorn api:app --port $port --host 0.0.0.0