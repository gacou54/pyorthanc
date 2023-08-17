
### Release 1.11.5 

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
