# First steps

## Orthanc installation
For testing purposes, you can use one of this solution to install Orthanc

- Orthanc's demo server (https://orthanc.uclouvain.be/demo)
- Deploy it locally with docker using `docker run -p 8042:8042 -p 4242:4242 orthancteam/orthanc`
- Using the docker-compose from the pyorthanc repo
    - For this, clone the repo (`git clone https://github.com/gacou54/pyorthanc`)
    - Got in the repo (`cd pyorthanc`)
    - Start orthanc (`docker compose up orthanc1`)
- Other method to install Orthanc are available [here](https://www.orthanc-server.com/download.php)

## PyOrthanc installation
```bash
pip install pyorthanc
pip install pyorthanc[all]  # (Optional) For progress bar when downloading DICOM data

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
import pyorthanc

pyorthanc.upload(orthanc, 'A_DICOM_INSTANCE_PATH.dcm')
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

# Retrieve (C-Move) results of query on a Orthanc itself, or to a target modality (AET)
modality.move(query_response['ID'])
# or
modality.move(query_response['ID'], {'TargetAet': 'OTHER_AET'})
```

### Find and download patients according to criteria:
```python
from pyorthanc import find_patients

patients = find_patients(
    client=orthanc,
    query={'PatientName': '*Gabriel'},  # Filter on PatientName
    labels=['a-label']  # Filter on patients with the 'a-label'
)
```

Download the patients data

```python
import os
from pyorthanc import retrieve_and_write_patients

os.makedirs('./data')  # Ensure that the target directory exists

for patient in patients:
    patient.download(f'./data/patient-{patient.patient_id}.zip', with_progres=False)

# As a directory tree DICOM files (patients -> studies -> series -> instances)
retrieve_and_write_patients(patients, './data/')
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

If you have the Patient ID, StudyInstanceUID, the SeriesInstanceUID
and/or the SOPInstanceUID, you can generate the Orthanc IDs:

```python
from pyorthanc import util, Patient

util.to_orthanc_patient_id('patient_id')  # '8dfa510b-b29ad31a-b2139fbf-b9929710-2edfa5c2'
util.to_orthanc_study_id('patient_id', 'study_uid')  # 'f9c33ef9-0bcdc38b-c216e9e8-8dbd62c1-28e4815c'
util.to_orthanc_series_id('patient_id', 'study_uid', 'series_uid')  # 'beceea8b-5424ff8c-3c76fe2e-edfed858-819fe6e1'
util.to_orthanc_instance_id('patient_id', 'study_uid', 'series_uid', 'instance_uid')  # '0e7848a0-4337f771-bda13733-150f651b-dfddd545'

patient = Patient('8dfa510b-b29ad31a-b2139fbf-b9929710-2edfa5c2', client)
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

#### Find resources with complex filters or filter on many resource levels
The `pyorthanc.find()` function allow to find resources with filters on many levels,
or with complex filter. Each filter function takes an object that correspond to the resource level
and should return a boolean value.

Note that when using the `find()` function, the children of the resources `Patient/Study/Series/Instance`
are only query once and then filtered accordingly to the provided filters.
```python
from datetime import datetime
from pyorthanc import find

patients = find(
    orthanc,
    patient_filter=lambda patient: patient.last_update > datetime(year=2023, month=10, day=1),
    study_filter=lambda study: 'thorax' in study.description.lower(),
    series_filter=lambda series: series.modality == 'CT'
)
```
__Note__ that this function may take a while to run since each resource level is filtered. 
Using `find()` on large Orthanc server is not recommended.


#### Develop with the Orthanc's Python Plugin
The `orthanc_sdk` is useful when developing with the Orthanc's Python Plugin,
it exposes `orthanc` module when available (i.e. used as an Orthanc script),
or expose the functions/classes signatures when not for linting and autocomplete.

Use it the same way you would use the Python Plugin:

```python
# Has the same signature as `import orthanc`
from pyorthanc import orthanc_sdk 

def on_get(output: orthanc_sdk.RestOutput, *_, **__):
    output.AnswerBuffer('ok', 'text/plain')

orthanc_sdk.RegisterRestCallback('/test', on_get)
```


### For examples of usage, see [this](../tutorial/examples.md)
