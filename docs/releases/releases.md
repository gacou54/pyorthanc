Lastest release : 1.12.1
------------

The Orthanc client has been regenerated on the Orthanc 1.12.1 version (source of the [changelist](https://hg.orthanc-server.com/orthanc/file/Orthanc-1.12.1/NEWS)).

From 1.12.1:

    - API version upgraded to 21
    - "/tools/create-dicom" can now be used to create Encapsulated 3D
    - Manufacturing Model IODs (MTL, OBJ, or STL)
    - Added a route to delete the output of an asynchronous job (right now
    - only for archive jobs): e.g. DELETE /jobs/../archive

From 1.12.0:

    - New URIs "/.../{id}/labels/{label}" to test/set/remove labels
    - "/patients/{id}", "/studies/{id}", "/series/{id}" and "/instances/{id}"
    - contain the "Labels" field
    - "/tools/find" now accepts the "Labels" and "LabelsConstraint" arguments
    - "/tools/labels" lists all the labels that are associated with any resource
    - "/system": added "UserMetadata" and "HasLabels"
    - Added option "?numeric" if listing metadata

Also, the new client has been generated with the simple-openapi-client 0.4.0, which implies:

    - Allow the client Orthanc to return raw responses
    - Update httpx dependencies

Details:

    - All tests made with unittest has been refactored to use pytest

Release 1.11.5 
------------

PyOrthanc v1.11.5 follow Orthanc version 1.11.3.

This release mostly improves the `find()` function.  It now takes an `Orthanc` object rather than an URL. This allows better control of the configuration for the connection to the Orthanc server.

For example:
```python
from pyorthanc import Orthanc, find

orthanc = Orthanc(url='http://localhost:8042/', username='username', password='password')
patients = find(
    orthanc=orthanc,
    series_filter=lambda s: s.modality == 'RTDOSE'  # Optional: filter with pyorthanc.Series object
)
```
