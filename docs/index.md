# PyOrthanc

**PyOrthanc** is a Python client for the [Orthanc](https://www.orthanc-server.com/) REST API. It provides:

- Complete wrapping of the Orthanc REST API methods
- High-level utilities for common DICOM operations
- Asynchronous client support
- Helper functions for working with DICOM data
- Integration with the Orthanc Python plugin

## Why PyOrthanc?
PyOrthanc makes it easy to work with DICOM medical images stored on Orthanc servers using Python - instead 
of dealing with the DICOM protocol directly or creating complex code to interact with Orthanc's REST API.

Researchers and clinicians can make simple Python script to access and manage their medical imaging data. 

Advanced users can use PyOrthanc to make Orthanc query a hospital PACS (Picture Archiving and Communication System).
This allows to find and retrieve images produced in the clinic for research or quality control purposes. 
Additionally, since PyOrthanc simplifies Orthanc's anonymization operations, 
an entire medical image management workflow can be implemented in Python.

## Quick Install

```bash
pip install pyorthanc        # Basic installation
pip install pyorthanc[all]   # Install all optional dependencies (progr)
```

## Basic Usage
```python
from pyorthanc import Orthanc

# Connect to Orthanc server
client = Orthanc('http://localhost:8042')
# Or with authentication:
client = Orthanc('http://localhost:8042', username='orthanc', password='orthanc')

# Basic operations
patient_ids = client.get_patients()
studies = client.get_studies() 

# Upload DICOM file
with open('image.dcm', 'rb') as f:
    client.post_instances(f.read())
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
response = modality.query({
    'Level': 'Study',
    'Query': {
        'PatientID': '12345*',
        'StudyDate': '20230101-20231231'
    }
})

# Retrieve results with C-MOVE to a target AET
modality.move(response['ID'], {'TargetAet': 'ORTHANC'})
```
## Finding and Processing DICOM Data

```python
from pyorthanc import find_patients

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
```

## Using pyorthanc within Orthanc

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


## [Cheat sheet](cheat_sheet.md)
## [First steps](tutorial/quickstart.md#first-steps)
### [Getting started](tutorial/quickstart.md#getting-started)
* [Import pyorthanc library](tutorial/quickstart.md#import-pyorthanc-library)
* [Connect to Orthanc](tutorial/quickstart.md#connect-to-orthanc)
* [Upload DICOM files to Orthanc:](tutorial/quickstart.md#upload-dicom-files-to-orthanc)
* [Getting list of connected remote modalities:](tutorial/quickstart.md#getting-list-of-connected-remote-modalities)
* [Find and download patients according to criteria:](tutorial/quickstart.md#find-and-download-patients-according-to-criteria)
* [Query (C-Find) and Retrieve (C-Move) from remote modality:](tutorial/quickstart.md#query-c-find-and-retrieve-c-move-from-remote-modality)
### [Examples](tutorial/examples.md)
* [Query and access data in an Orthanc Sever](tutorial/examples.md#find-data-on-your-orthanc-server)
* [Interact with a connected modality](tutorial/examples.md#orthanc-as-a-tool-to-query-and-retrieve-data-from-the-hospital-pacs)
* [Transfer data from a PACS to an Orthanc server](tutorial/examples.md#transfer-data-from-a-pacs-to-an-orthanc-server)
### [Community guidelines](contributing.md)
* [Report an issue](contributing.md#report-an-issue)
* [Support](contributing.md#seeking-support)
* [Contribute](contributing.md#contribute)
### [Releases](releases.md)
## [Contacts](contacts.md#contacts)
* [Maintainers Team](contacts.md#maintainers-team)
* [Useful links](contacts.md#useful-links)
## [Citation](citation.md#citation)
