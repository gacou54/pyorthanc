PyOrthanc
=========
Python library that wrap the Orthanc REST API and facilitate the manipulation of data.

Link to Orthanc web site: https://www.orthanc-server.com/

__Notes__:
Please note that this is an early version of the wrapper (version < 1.0),
therefore some methods description (and maybe name) may change because 
they don't describe adequately the behavior of the corresponding Orthanc REST API route.
Also note that this librairy is still under development.
If the description of an `Orthanc` method does not correspond to the planned 
behavior, please do an issue.

However, 'PyOrthanc' contains objects and functions that may be
useful for anyone writing python script to interact with Orthanc.

Also note that tests (```python setup.py test```) might only work
on a linux machine.


Installation
------------
```sh
$ pip install pyorthanc
```

Or from the repository:
```sh
pip install git+https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc.git
```

Or, if you do not have git installed, clone the repository:
```sh
pip install -e pyorthanc.zip
```

#### Specific version
If you are looking for a specific version, lookout the version with the desired 
tag ar https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc/tags.

Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

#### With Orthanc server:
```python
from pyorthanc import Orthanc


orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

# To get patients identifier and main information
patients_identifiers = orthanc.get_patients()

for patient_identifier in patients_identifiers:
    patient_information = orthanc.get_patient_information(patient_identifier)


# To get patient's studies identifier and main information
a_patient_identifier = patients_identifiers[0]
studies_identifiers = orthanc.get_studies(a_patient_identifier)

for study_identifier in studies_identifiers:
    study_information = orthanc.get_studies_information(study_identifier)
```

#### Upload DICOM files to Orthanc:
```python
from pyorthanc import Orthanc


orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

with open('A_DICOM_INSTANCE_PATH.dcm', 'rb') as file_handler:
    orthanc.post_instances(file_handler.read())

```

#### Getting list of remote modalities:
```python
from pyorthanc import Orthanc


orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

orthanc.get_modalities()
```

#### Query (C-Find) and Retrieve (C-Move) from remote modality:
```python
from pyorthanc import RemoteModality, Orthanc


remote_modality = RemoteModality(Orthanc('http://localhost:8042'), 'modality')
remote_modality.setup_credentials('username', 'password')  # If needed

# Query (C-Find) on modality
data = {'Level': 'Study', 'Query': {'PatientID': '*'}}
query_response = remote_modality.query(data=data)

# Retrieve (C-Move) results of query on a target modality (AET)
remote_modality.move(query_response['QUERY_ID'], 'target_modality')
```

#### Build a patient tree structure of all patients in Orthanc instance:
Each patient is a tree. Layers in each tree are `Patient` -> `Study` -> `Series` -> `Instance`.
```python
from pyorthanc import Orthanc, build_patient_forest


patient_forest = build_patient_forest(
    Orthanc('http://localhost:8042/')
)    

for patient in patient_forest:
    patient_info = patient.get_main_information()
    
    for study in patient.get_studies():
        ...
```

#### Anonymize patient and get file:
```python
from pyorthanc import Orthanc


orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

A_PATIENT_IDENTIFIER = orthanc.get_patients()[0]

orthanc.anonymize_patient(A_PATIENT_IDENTIFIER)

# result is: (you can retrieve DICOM file from ID)
# {'ID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Path': '/patients/dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'PatientID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Type': 'Patient'}
```
