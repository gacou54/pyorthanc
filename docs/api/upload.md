# Upload

The Orthanc REST API is commonly used to upload DICOM files.
To do so, you can use the `upload()` function.

```python
from pyorthanc import Orthanc, upload

orthanc = Orthanc(url='http://localhost:8042')

# The file can be a DICOM file, a zip file containing one or multiple DICOM
upload(orthanc, 'dicom_filepath.dcm')

# You can also upload a zip file containing one or multiple DICOM
upload(orthanc, 'dicoms.zip')

# A directory path can be also used. All DICOM files from the directory will be uploaded
upload(orthanc, 'directory/path')
upload(orthanc, 'directory/path', recursive=True)  # For nested dicom files

# Note that `upload` returns a list of the uploaded instances `list[pyorthanc.Instance]`
instances = upload(orthanc, 'directory/path')
print(instances)
```

## Avoid uploading the same file twice
DICOM files are often big, and uploading them multiple times can be time-consuming.
To avoid uploading the same file twice, you can use the `check_before_upload` option.

Note that ZIP files will always be re-uploaded.

```python
from pyorthanc import Orthanc, upload

orthanc = Orthanc(url='http://localhost:8042')

# For each DICOM file, it will check if the file is in Orthanc before uploading it.
upload(orthanc, 'directory/path', recursive=True, check_before_upload=True)
```

## Reference
::: pyorthanc._upload
options:
members: true
:docstring:
:members:
