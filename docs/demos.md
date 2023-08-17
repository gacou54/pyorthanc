

Installation
------------
```sh
$ pip install pyorthanc
```

Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

#### Getting access to patients, studies, series and instances information:

```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042', username='username', password='password')

# To get patients identifier and main information
patients_identifiers = orthanc.get_patients()

for patient_identifier in patients_identifiers:
   # To get patient information
   patient_info = orthanc.get_patients_id(patient_identifier)

   patient_name = patient_info['MainDicomTags']['PatientName']
   ...
   study_identifiers = patient_info['Studies']

# To get patient's studies identifier and main information
for study_identifier in study_identifiers:
   # To get Study info
   study_info = orthanc.get_studies_id(study_identifier)

   study_date = study_info['MainDicomTags']['StudyDate']
   ...
   series_identifiers = study_info['Series']

# To get study's series identifier and main information
for series_identifier in series_identifiers:
   # Get series info
   series_info = orthanc.get_series_id(series_identifier)

   modality = series_info['MainDicomTags']['Modality']
   ...
   instance_identifiers = series_info['Instances']

# and so on ...
for instance_identifier in instance_identifiers:
   instance_info = orthanc.get_instances_id(instance_identifier)
   ...
```

#### Find patients with certain characteristics in an Orthanc instance:
Each patient is a tree. Layers in each tree have the following structure 
`Patient` -> `Study` -> `Series` -> `Instance`
that correspond to the provided filter functions.

```python
from pyorthanc import find, Orthanc

orthanc = Orthanc(url='http://localhost:8042/', username='username', password='password')
patients = find(
    orthanc=orthanc,
    series_filter=lambda s: s.modality == 'RTDOSE'  # Optional: filter with pyorthanc.Series object
)

for patient in patients:
   patient_info = patient.get_main_information()
   patient.id_   # Access PatientID
   patient.name  # Access PatientName
   
   patient.get_zip() # DICOM files' content in bytes
   
   anonymized_patient_1 = patient.anonymize()  # New patient that was anonymized by Orthanc
   anonymized_patient_2 = patient.anonymize(
      keep=['PatientName'],   # You can keep/remove/replace the DICOM tags you want
      replace={'PatientID': 'TheNewPatientID'},
      remove=['ReferringPhysicianName'],
      force=True  # Needed when changing PatientID/StudyInstanceUID/SeriesInstanceUID/SOPInstanceUID
   )  
   ...

   for study in patient.studies:
       study.date  # Date as a datetime object
       study.referring_physician_name
       ...

       for series in study.series:
           series.modality  # Should be 'RTDOSE' because of the series_filter parameters
           ...
           for instance in series.instances:
               # Getting content by tag
               instance.get_content_by_tag('ManufacturerModelName')  # == 'Pinnable3'
               # Or
               instance.get_content_by_tag('0008-1090')  # == 'Pinnable3'

               pydicom_dataset = instance.get_pydicom()  # Retrieve the DICOM file and make a pydicom.FileDataset
               pydicom_dataset.pixel_array  # You can access the pydicom.FileDataset attribute
        
```


#### Upload DICOM files to Orthanc:

```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042', 'username', 'password')

with open('A_DICOM_INSTANCE_PATH.dcm', 'rb') as file:
   orthanc.post_instances(file.read())
```

#### Getting list of connected remote modalities:
```python
from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042', 'username', 'password')

orthanc.get_modalities()
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

#### Transfer data from a PACS to a Orthanc server:

[dicom-transfer](https://github.com/ylemarechal/dicom-transfer)