cd ~/PiPrint
source venv/bin/activate
uvicorn api:app --host 0.0.0.0

#chmod +x ~/PiPrint/run-server-network.sh