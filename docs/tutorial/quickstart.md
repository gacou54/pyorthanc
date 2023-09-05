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
### Query (C-Find) and Retrieve (C-Move) from remote modality:

```python
from pyorthanc import Modality

modality = Modality(orthanc, 'modality')

# C-Echo
assert modality.echo()  # Test the connection

# Query (C-Find) on modality
data = {'Level': 'Study', 'Query': {'PatientID': '*'}}
query_response = modality.query(data=data)

# Inspect the answer
answer = modality.get_query_answers()[query_response['ID']]
print(answer)

# Retrieve (C-Move) results of query on a target modality (AET)
modality.move(query_response['ID'], {'TargetAet': 'target_modality'})
```

### Find and download patients according to criteria:
```python
from pyorthanc import find_patients, retrieve_and_write_patients

patients = find_patients(
    client=orthanc,
    query={'PatientName': '*Gabriel'},  # Filter on PatientName
    labels=['a-label']  # Filter on patients with the 'a-label'
)
```

Write the patients DICOM files locally
```python
retrieve_and_write_patients(patients, './patients_path')
```
Or manipulates the Patient object
```python
patient = patients[0]

patient.name
patient.is_stable
patient.last_update

patient.labels
patient.remove_label('a-label')
patient.add_label('a-new-label')
...
```

It is also possible to query the other resource levels
```python
from pyorthanc import find_studies, find_series, find_instances

studies = find_studies(client=orthanc, query={...}, labels=[...])
series = find_series(client=orthanc, query={...}, labels=[...])
instances = find_instances(client=orthanc, query={...}, labels=[...])
```

#### Anonymize patient
Resources (`Patient`, `Study`, `Series`, `Instance`) can be easily __anonymized__.
```python
import pyorthanc

orthanc_patient_id = client.get_patients()[0]
patient = pyorthanc.Patient(orthanc_patient_id, client)
```
Waiting for the anonymization process (this may raise a TimeOutError)
```python
new_patient = patient.anonymize()
new_patient_with_given_patient_id = patient.anonymize(
   keep=['PatientName'],
   replace={'PatientID': 'TheNewPatientID'},
   force=True  # Needed when changing PatientID/StudyInstanceUID/SeriesInstanceUID/SOPInstanceUID
)
```
For long-running job (i.e. large patient) or to submit many anonymization jobs at the same time, use
```python
job = patient.anonymize_as_job()
job.state  # You can follow the job state

job.wait_until_completion() # Or just wait on its completion
new_patient = pyorthanc.Patient(job.content['ID'], client)
```


## Full basic examples

Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

Here is a list of examples to helps you getting started with pyorthanc.

### Access instance information

[Get instance informations](https://github.com/ylemarechal/pyorthanc-examples/tree/main/basic/access_informations)
