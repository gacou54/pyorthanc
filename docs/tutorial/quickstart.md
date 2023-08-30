# First steps

## Requirements

- [x] Python3.8

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pyorthanc
```
## Getting started 
### Import pyorthanc library
```python
import pyorthanc
```

### Connect to Orthanc
Here are some quick how to examples to use pyorthanc
```python
from pyorthanc import Orthanc

orthanc = Orthanc(url='http://localhost:8042/', 
                  username='username', 
                  password='password')
```


### Upload DICOM files to Orthanc:

```python
from pyorthanc import Orthanc

orthanc = Orthanc(url='http://localhost:8042/', 
                  username='username', 
                  password='password')

with open('A_DICOM_INSTANCE_PATH.dcm', 'rb') as file:
   orthanc.post_instances(file.read())
```
### Getting list of connected remote modalities:
```python
from pyorthanc import Orthanc

orthanc = Orthanc(url='http://localhost:8042/', 
                  username='username', 
                  password='password')

orthanc.get_modalities()
```

Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

Here is a list of examples to helps you getting started with pyorthanc

| code                                                                                                            | 
|-----------------------------------------------------------------------------------------------------------------|
| [Access instance informations](https://github.com/ylemarechal/pyorthanc/tree/main/examples/access_informations) |

## Some useful commands

### Docker commands
Start Orthanc
```bash
docker compose up -d
```
Stop Orthanc
```bash
docker compose stop
```
Restart Orthanc
```bash
docker compose restart
```
Delete Orthanc container
```bash
docker compose down
```