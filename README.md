# PiPrint
Simple print server for RPi

## Start the server


* To only listen on local machine: ```uvicorn api:app```
* To listen to all devices on local network: ```uvicorn api:app --host 0.0.0.0```

## Uploading a file to the server

### Python (requests)
* Template
  * ```requests.post(<url>,files = dict(file = open(<filename.zpl>,'rb')))```
* Example
  * ```requests.post('http://localhost:8000/zebra/api/upload-file',files = dict(file = open(MyLabel.zpl,'rb')))```

### cURL
* __Template__
    * ```curl <URL> -F file=@<path/to/file>```
* __Example__
  * ```curl http://127.0.0.1:8000/upload-file/ -F file=@mylabel.zpl```


## Printing a label
### Python (requests)
* ```requests.post(baseurl/print-label/<label-to-print>)```
* ```requests.post('http://localhost:8000/zebra/api/print-label/mylabel')```
### cURL
* ```curl -X POST baseurl/print-label/<label-to-print>```  
* ```curl -X POST 'http://localhost:8000/zebra/api/print-label/mylabel'```

## Printing a label with variables
### Python (requests)
* ```requests.post(base/url<label-to-print>,json = {'formatters':dict(var1=val1,var2=val2)})```

### cURL
* __Template__
  * ```curl -X POST <url> -H 'content-Type: application/json' -d <JSON Data>```  
* __Example__
  * ```curl -X POST http://127.0.0.1:8000/print-label/ -H 'Content-Type: application/json' -d '{"name":"mylabel","formatters":{"variable1":"value1","variable2":"value2"}}'```