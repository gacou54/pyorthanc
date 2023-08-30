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

### Find and download patients according to criteria:

```python
from pyorthanc import Orthanc, find_patients, retrieve_and_write_patients

orthanc = Orthanc(url='https://demo.orthanc-server.com', username='', password='')

patients = find_patients(
    client=orthanc,
    query={'PatientName': 'COMUNIX'} # Optional: filter with pyorthanc.Series object
)
retrieve_and_write_patients(patients, '.')
```

#### Query (C-Find) and Retrieve (C-Move) from remote modality:

```python
from pyorthanc import RemoteModality, Orthanc

orthanc = Orthanc('http://localhost:8042', 'username', 'password')

modality = RemoteModality(orthanc, 'modality')

# Query (C-Find) on modality
data = {'Level': 'Study', 'Query': {'PatientID': '*'}}
query_response = modality.query(data=data)

answer = modality.get_query_answers()[query_response['ID']]
print(answer)

# Retrieve (C-Move) results of query on a target modality (AET)
modality.move(query_response['ID'], {'TargetAet': 'target_modality'})
```

#### Anonymize patient:
```python
from pyorthanc import Orthanc, Patient

orthanc = Orthanc('http://localhost:8042', 'username', 'password')

patient_identifier = orthanc.get_patients()[0]

anonymized_patient = Patient(patient_identifier, orthanc).anonymize(
    keep=['PatientName'],   # You can keep/remove/replace the DICOM tags you want
    replace={'PatientID': 'TheNewPatientID'},
    remove=['ReferringPhysicianName'],
    force=True  # Needed when changing PatientID/StudyInstanceUID/SeriesInstanceUID/SOPInstanceUID
)
# Or directly with
orthanc.post_patients_id_anonymize(patient_identifier)

# result is: (you can retrieve DICOM file from ID)
# {'ID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Path': '/patients/dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'PatientID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Type': 'Patient'}
```

Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

Here is a list of examples to helps you getting started with pyorthanc

| code                                                                                                            | 
|-----------------------------------------------------------------------------------------------------------------|
| [Access instance informations](https://github.com/ylemarechal/pyorthanc-examples/tree/main/basic/access_informations) |

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