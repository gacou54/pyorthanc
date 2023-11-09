[![ci](https://github.com/gacou54/pyorthanc/workflows/Test/badge.svg)](https://github.com/gacou54/pyorthanc/actions?query=workflow%3ATest)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://gacou54.github.io/pyorthanc/)
![PyPI - Version](https://img.shields.io/pypi/v/pyorthanc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyorthanc)
# PyOrthanc
**PyOrthanc** is a python client for the Orthanc REST API, which fully wraps all the methods of the REST API.
Additionally, it provides many utility functions to interact with an Orthanc instance.

See the full documentation here https://gacou54.github.io/pyorthanc

---
Install PyOrthanc using pip:
```bash
pip install pyorthanc
```
---
Then use the client. If Orthanc is running locally, the default URL is `http://localhost:8042`.
```python
import pyorthanc

client = pyorthanc.Orthanc('http://localhost:8042', username='orthanc', password='orthanc')
patient_ids = client.get_patients()
```

Interact with connected modalities
```python
import pyorthanc

modality = pyorthanc.Modality(client, 'MY_MODALITY')
assert modality.echo()

# C-Find on modality
response = modality.query({'Level': 'Study', 'Query': {'PatientID': '*'}})

# C-Move to target modality
modality.move(response['ID'], {'TargetAet': 'target_modality'})
```
Find patients
```python
patients = pyorthanc.find_patients(client, {'PatientID': '*P001'})
for patient in patients:
    patient.labels
    patient.is_stable
    patient.name
    ...
    for study in patient.studies:
        study.labels
        study.date
        ...
        for series in study.series:
            ...
            for instance in series.instances:
                pydicom_ds = instance.get_pydicom()
```

Resources (`Patient`, `Study`, `Series`, `Instance`) can be easily __anonymized__.
```python
import pyorthanc

orthanc_patient_id = client.get_patients()[0]
patient = pyorthanc.Patient(orthanc_patient_id, client)
```
Waiting the for the anonymization process:
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

## Notes on versioning

The `Orthanc` and `AsyncOrthanc` classes are generated from `https://api.orthanc-server.com/`.

Compatibility of versions between PyOrthanc and the Orthanc REST API are the following.
Note that recent PyOrthanc versions will likely support older Orthanc version.

| PyOrthanc version | Generated from                                |
|-------------------|-----------------------------------------------|
| \>= 1.13.2        | Orthanc API 1.12.1 with Python Plugin 4.1     |
| 1.13.0, 1.13.1    | Orthanc API 1.12.1 with Python Plugin 4.0     |
| 1.12.*            | Orthanc API 1.12.1                            |
| 1.11.*            | Orthanc API 1.11.3                            |
| 0.2.*             | Provided Google sheet from Orthanc maintainer |


You can still use the old client with
```python
from pyorthanc.deprecated.client import Orthanc  # Old client wrote by hand
from pyorthanc.deprecated.client_1_11_3 import Orthanc
```

Note that due to automatic generation some method names may be less clear.
However, the automatic generation allows PyOrthanc to cover all the routes of the API of Orthanc.


## Citation
If you publish using PyOrthanc, we kindly ask that you credit us. PyOrthanc can be found on Zenodo :
https://zenodo.org/record/7086219 .

## Credits
The `orthanc_sdk.py` has been generated from the `scripts/data/python-sdk.txt` file,
which is from the [Python Orthanc Plugin](https://github.com/orthanc-server/orthanc-setup-samples/blob/master/python-samples/python-sdk.txt)

## Contributing
You can contribute to this project with the following steps:
1. First, fork the project on Github 
2. Clone the project
   ```shell
   git clone https://github.com/<your-github-username>/pyorthanc
   cd pyorthanc
   ```
3. Create a poetry environment 
   (this project use the [poetry](https://python-poetry.org/) for dependency management)
   ```shell
   peotry install 
   ```
4. Make a new git branch where you will apply the changes
   ```shell
   git checkout -b your-branch-name
   ```
   Now you can make your changes
5. Once done, `git add`, `git commit` and `git push` the changes.
6. Make a Pull Request from your branch to the https://github.com/gacou54/pyorthanc.

