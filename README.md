[![ci](https://github.com/gacou54/pyorthanc/workflows/Test/badge.svg)](https://github.com/gacou54/pyorthanc/actions?query=workflow%3ATest)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://gacou54.github.io/pyorthanc/)
![PyPI - Version](https://img.shields.io/pypi/v/pyorthanc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyorthanc)
[![status](https://joss.theoj.org/papers/73f4c5a5e026aa4ef0e7ed9ed471a9a7/status.svg)](https://joss.theoj.org/papers/73f4c5a5e026aa4ef0e7ed9ed471a9a7)

# PyOrthanc

**PyOrthanc** is a comprehensive Python client for [Orthanc](https://www.orthanc-server.com/), providing:

- Complete wrapping of the Orthanc REST API methods
- High-level utilities for common DICOM operations 
- Asynchronous client support
- Helper functions for working with DICOM data
- Integration with the [Orthanc Python plugin](https://orthanc.uclouvain.be/book/plugins/python.html)


## Why PyOrthanc?
PyOrthanc makes it easy to work with DICOM medical images stored on Orthanc servers using Python - instead
of dealing with the DICOM protocol directly or creating complex code to interact with Orthanc's REST API.

Researchers and clinicians can make simple Python script to access and manage their medical imaging data.

Advanced users can use PyOrthanc to make Orthanc query a hospital PACS (Picture Archiving and Communication System).
This allows to find and retrieve images produced in the clinic for research or quality control purposes.
Additionally, since PyOrthanc simplifies Orthanc's anonymization operations,
an entire medical image management workflow can be implemented in Python.

## PyOrthanc or python-orthanc-api-client? 

Another project [`python-orthanc-api-client`](https://github.com/orthanc-team/python-orthanc-api-client) 
from [orthanc-team](https://github.com/orthanc-team) is quite similar to `pyorthanc`. 

If you are wondering which one to use, please refer to this [discussion](https://github.com/gacou54/pyorthanc/issues/80).

## Quick Install
```bash
pip install pyorthanc        # Basic installation
pip install pyorthanc[all]   # Install all optional dependencies
```

## Basic Usage
Assuming an Orthanc server running locally at `http://localhost:8042`:
```python
from pyorthanc import Orthanc, upload

# Connect to Orthanc server
client = Orthanc('http://localhost:8042')
# Or with authentication:
client = Orthanc('http://localhost:8042', username='orthanc', password='orthanc')

# Basic operations
patient_ids = client.get_patients()
studies = client.get_studies() 

# Upload DICOM files
upload(client, 'image.dcm')  # From a file
upload(client, 'dicom_files.zip')  # From a zip
upload(client, 'path/to/directory')  # Upload all dicom files in a directory
upload(client, 'path/to/directory', recursive=True)  # Upload all dicom files in a directory recursively
# Check if dicom is in Orthanc before upload
upload(client, 'path/to/directory', recursive=True, check_before_upload=True)
```

## Working with DICOM Modalities

```python
from pyorthanc import Modality

# Create modality connection
modality = Modality(client, 'REMOTE_PACS')

# Test connection with C-ECHO
if modality.echo():
    print("Successfully connected to PACS")

# Query studies with C-FIND
response = modality.find({
    'Level': 'Study',
    'Query': {
        'PatientID': '12345*',
        'StudyDate': '20230101-20231231'
    }
})

# Matches (i.e. answers in Orthanc nomenclature) can be reviewed before retrieving results
response['answers']

# Retrieve results with C-MOVE to a target AET
modality.move(response['ID'], {'TargetAet': 'ORTHANC'})
```

## Finding and Processing DICOM Data

```python
from pyorthanc import find_patients, find_studies, find_series, find_instances

# Search for patients
patients = find_patients(
    client,
    query={'PatientName': '*Gabriel'},
    labels=['research']  # It is also possible to filter by labels
)

# Process patient data
for patient in patients:
    print(f"Patient: {patient.name} (ID: {patient.patient_id})")
    print(f"Birth Date: {patient.birth_date}")
    print(f"Labels: {patient.labels}")
    
    # Access studies
    for study in patient.studies:
        print(f"\nStudy Date: {study.date}")
        print(f"Description: {study.description}")
        
        # Access series
        for series in study.series:
            print(f"\nModality: {series.modality}")
            print(f"Series Description: {series.description}")
            
            # Access individual DICOM instances
            for instance in series.instances:
                # Convert to pydicom dataset
                ds = instance.get_pydicom()
                # Process DICOM data...

# Note the existing function to query Orthanc
find_studies(client, query={...})
find_series(client, query={...})
find_instances(client, query={...})
```

## Using pyorthanc within Orthanc's Python plugin

Use the `orthanc_sdk` module when using [Orthanc's Python plugin](https://orthanc.uclouvain.be/book/plugins/python.html).
`orthanc_sdk` acts as the same as `orthanc`, but it provides type hints and autocompletion. 
For example:

```python
from pyorthanc import orthanc_sdk

# Register a new REST endpoint
def handle_api(output: orthanc_sdk.RestOutput, uri: str, **request):
    """Handle REST API request"""
    if request['method'] == 'GET':
        output.AnswerBuffer('Hello from plugin!', 'text/plain')
    else:
        output.SendMethodNotAllowed('GET')

orthanc_sdk.RegisterRestCallback('/hello-world', handle_api)

# Handle incoming DICOM
def on_store(dicom: orthanc_sdk.DicomInstance, instance_id: str):
    """Process stored DICOM instances"""
    print(f'Received instance {instance_id}')
    print(f'Size: {dicom.GetInstanceSize()} bytes')
    print(f'Transfer Syntax: {dicom.GetInstanceTransferSyntaxUid()}')

orthanc_sdk.RegisterOnStoredInstanceCallback(on_store)
```

## Examples
Typical example can be found in these notebooks.
-  This [notebook](https://github.com/gacou54/pyorthanc/blob/main/examples/find_data.ipynb) shows
   how a user can query image data from an Orthanc server
-  This [notebook](https://github.com/gacou54/pyorthanc/blob/main/examples/modalities.ipynb) shows
   how a user can query and pull data from other modality (such as a CT scan or a PACS) connected to an Orthanc Server. 


## Notes on versioning

The `Orthanc` and `AsyncOrthanc` classes are generated from https://orthanc.uclouvain.be/api/.

Compatibility of versions between PyOrthanc and the Orthanc REST API are the following.
Note that recent PyOrthanc versions will likely support older Orthanc version.

| PyOrthanc version | Generated from                                |
|-------------------|-----------------------------------------------|
| \>= 1.20.0        | Orthanc API 1.12.6 with Python Plugin 4.2     |
| 1.19.0, 1.19.1    | Orthanc API 1.12.5 with Python Plugin 4.2     |
| 1.18.0            | Orthanc API 1.12.4 with Python Plugin 4.2     |
| 1.17.0            | Orthanc API 1.12.3 with Python Plugin 4.2     |
| 1.13.2 to 1.16.1  | Orthanc API 1.12.1 with Python Plugin 4.1     |
| 1.13.0, 1.13.1    | Orthanc API 1.12.1 with Python Plugin 4.0     |
| 1.12.*            | Orthanc API 1.12.1                            |
| 1.11.*            | Orthanc API 1.11.3                            |
| 0.2.*             | Provided Google sheet from Orthanc maintainer |


## Running tests
The tests are run in a docker image launched with docker compose.

```shell
docker compose run test
```
This command starts 3 containers :
1. A Python image with the PyOrthanc source code and launches pytest
2. An instance of Orthanc (`orthanc1`) on which the PyOrthanc client is connected
3. A second Orthanc instance (`orthanc2`) which acts as a modality connected to `orthanc1`

## [Cheat sheet](docs/cheat_sheet.md)
## [First steps](docs/tutorial/quickstart.md#first-steps)
### [Getting started](docs/tutorial/quickstart.md#getting-started)
* [Connect to Orthanc](docs/tutorial/quickstart.md#connect-to-orthanc)
* [Upload DICOM files to Orthanc](docs/tutorial/quickstart.md#upload-dicom-files-to-orthanc)
* [Handle connected DICOM modalities](docs/tutorial/quickstart.md#getting-list-of-connected-remote-modalities)
* [Find and download patients according to criteria](docs/tutorial/quickstart.md#find-and-download-patients-according-to-criteria)
* [Query (C-Find) and Retrieve (C-Move) from remote modality](docs/tutorial/quickstart.md#query-c-find-and-retrieve-c-move-from-remote-modality)
### [Advanced examples](docs/tutorial/advanced.md)
### [Releases](https://github.com/gacou54/pyorthanc/releases)
### [Community guidelines](docs/contributing.md)
* [Report an issue](docs/contributing.md#report-an-issue)
* [Support](docs/contributing.md#seeking-support)
* [Contribute](docs/contributing.md#contribute)
## [Contacts](docs/contacts.md#contacts)
* [Maintainers Team](docs/contacts.md#maintainers-team)
* [Useful links](docs/contacts.md#useful-links)
## [Citation](docs/citation.md#citation)
