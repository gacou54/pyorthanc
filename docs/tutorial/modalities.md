# Communicates with modalities connected to Orthanc

Orthanc is often used to interact with other DICOM modalities/PACS in clinical or 
research environment, and pyorthanc makes this easy.

![Modality diagram](docs/img/diagrams.png)

You can first find the connected modality to your Orthanc instance:
```python
from pyorthanc import Orthanc

orthanc = Orthanc(url='http://localhost:8042/', username='orthanc', password='orthanc')

modalities = orthanc.get_modalities()
print(modalities)
```

## The Modality class
The `Modality` class allows you to send the common DICOM requests to a particular modality, 
such as the C-Echo, C-Find, C-Move and C-Store.
```python
from pyorthanc import Modality

modality = Modality(orthanc, 'modality-name')
```

### Assert the connection (C-Echo)
Perform a C-Echo to test the connection between Orthanc and the modality
```python
assert modality.echo()  # Returns True or False
```

### Query the modality (C-Find)
Querying the modality from Orthanc will create "Query Answer" inside Orthanc
```python
query_response = modality.query(
    data={'Level': 'Study', 'Query': {'PatientID': '*'}}
)
```
It is then possible to review the Query Answer to see if the C-Find actually found something
````python
answer =  modality.get_query_answers()[query_response['ID']]
print(answer)
````

### 