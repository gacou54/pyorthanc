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

To check if a file is in Orthanc, `pyorthanc` reads it with `pydicom`. Files that are not valid DICOM Part 10
files (e.g. without the 128-byte preamble and the "DICM" prefix) cannot be read, so they are always uploaded.
Use `force=True` to read them with `pydicom.dcmread(..., force=True)` and check them as well.

```python
upload(orthanc, 'directory/path', check_before_upload=True, force=True)
```

## Asynchronous upload
`async_upload()` takes the same options as `upload()`, with an `AsyncOrthanc` client.
It returns the Orthanc identifiers of the instances (`list[str]`).

```python
from pyorthanc import AsyncOrthanc, async_upload

async_orthanc = AsyncOrthanc(url='http://localhost:8042')

instance_ids = await async_upload(async_orthanc, 'directory/path', recursive=True, check_before_upload=True)
```

## Reference
::: pyorthanc._upload
options:
members: true
:docstring:
:members:
