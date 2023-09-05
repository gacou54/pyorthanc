# First steps

## Installation
```bash
pip install pyorthanc
```
## Getting started 
### Connect to Orthanc
Here are some quick how to examples to use pyorthanc
```python
from pyorthanc import Orthanc

orthanc = Orthanc(url='http://localhost:8042/', username='orthanc', password='orthanc')
```

### Upload DICOM files to Orthanc:
```python
with open('A_DICOM_INSTANCE_PATH.dcm', 'rb') as file:
    orthanc.post_instances(file.read())
```
### Getting list of connected remote modalities:
```python
modalities = orthanc.get_modalities()
```

### Find and download patients according to criteria:
```python
from pyorthanc import find_patients, retrieve_and_write_patients

patients = find_patients(
    client=orthanc,
    query={'PatientName': 'COMUNIX'} # Optional: filter with pyorthanc.Series object
)
retrieve_and_write_patients(patients, './patients_path')
```

### Query (C-Find) and Retrieve (C-Move) from remote modality:

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
from pyorthanc import Patient

patient_identifier = orthanc.get_patients()[0]
patient = Patient(patient_identifier, orthanc)

anonymized_patient = patient.anonymize(
    keep=['PatientName'],   # You can keep/remove/replace the DICOM tags you want
    replace={'PatientID': 'TheNewPatientID'},
    remove=['ReferringPhysicianName'],
    force=True  # Needed when changing PatientID/StudyInstanceUID/SeriesInstanceUID/SOPInstanceUID
)
```

## Full basic examples

Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

Here is a list of examples to helps you getting started with pyorthanc.

### Access instance information

[Get instance informations](https://github.com/ylemarechal/pyorthanc-examples/tree/main/basic/access_informations)
