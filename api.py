import datetime as dt
from signal import raise_signal
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI, UploadFile, status, HTTPException
from zebra_printer import ZebraPrinter

BASE_URL = '/zebra/api'

app = FastAPI(root_path='')

z = ZebraPrinter()

# Define model for JSON Body
class PrintJob(BaseModel):
    formatters: dict = {}

# Define index
@app.get(f"{BASE_URL}/")
async def root():
    return {"message": "Hello World"}

# Print a test label
@app.get(f"{BASE_URL}/print-test/")
async def print_test():
    z.print_test_label()

# Get a list of available labels
@app.get(f"{BASE_URL}/label-list/")
async def label_list():
    return {"labels":list(z.label_files)}

# Print a defined label (label definition previously uploaded)
@app.post(f"{BASE_URL}/print-label/{{label_name}}")
async def print_label(label_name: str,job: PrintJob = PrintJob(), count: int = 1):

    # Make sure the requested label exists
    if label_name not in z.label_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{label_name} does not exist. Please upload the .zpl file')

    # Try printing the label
    try:
        z.print_label(label_name,n=count,**job.formatters)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect formatters passed')

# Upload a .zpl file defining a custom label
@app.post(f"{BASE_URL}/upload-file/",status_code = status.HTTP_201_CREATED)
async def upload_file(file: UploadFile):
    name = file.filename
    if '.zpl' not in name:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'{name} is not a .zpl file')
    content = await file.read()
    z.store_new_file(name,content)
