PyOrthanc
=========
Python library that wraps the Orthanc REST API and facilitates the manipulation
of data with several cool utilities.


Installation
------------
```sh
$ pip install pyorthanc
```

#### Specific version
If you are looking for a specific version, look here: https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc/tags.

Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

#### Getting access to patients, studies, series and instances information:
```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

# To get patients identifier and main information
patients_identifiers = orthanc.get_patients()

for patient_identifier in patients_identifiers:
    patient_information = orthanc.get_patient_information(patient_identifier)

    patient_name = patient_information['MainDicomTags']['name']
    ...
    study_identifiers = patient_information['Studies']    

# To get patient's studies identifier and main information
for study_identifier in study_identifiers:
    study_information = orthanc.get_study_information(study_identifier)
    
    study_date = study_information['MainDicomTags']['StudyDate']
    ...
    series_identifiers = study_information['Series']

# To get study's series identifier and main information
for series_identifier in series_identifiers:
    series_information = orthanc.get_series_information(series_identifier)
    
    modality = series_information['MainDicomTags']['Modality']
    ...
    instance_identifiers = series_information['Instances']

# and so on ...
for instance_identifier in instance_identifiers:
    instance_information = orthanc.get_instance_information(instance_identifier)
    ...
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
    patient.get_name()
    patient.get_zip()
    ...
    
    for study in patient.get_studies():
        study.get_date()
        study.get_referring_physician_name()
        ...

        for series in study.get_series():
            ...
```


#### Upload DICOM files to Orthanc:
```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

with open('A_DICOM_INSTANCE_PATH.dcm', 'rb') as file_handler:
    orthanc.post_instances(file_handler.read())
```

#### Getting list of connected remote modalities:
```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

orthanc.get_modalities()
```

#### Query (C-Find) and Retrieve (C-Move) from remote modality:
```python
from pyorthanc import RemoteModality, Orthanc

orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

remote_modality = RemoteModality(orthanc, 'modality')

# Query (C-Find) on modality
data = {'Level': 'Study', 'Query': {'PatientID': '*'}}
query_response = remote_modality.query(data=data)

# Retrieve (C-Move) results of query on a target modality (AET)
remote_modality.move(query_response['QUERY_ID'], 'target_modality')
```

#### Anonymize patient and get file:
```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042')
orthanc.setup_credentials('username', 'password')  # If needed

a_patient_identifier = orthanc.get_patients()[0]

orthanc.anonymize_patient(a_patient_identifier)

# result is: (you can retrieve DICOM file from ID)
# {'ID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Path': '/patients/dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'PatientID': 'dd41f2f1-24838e1e-f01746fc-9715072f-189eb0a2',
#  'Type': 'Patient'}
```
