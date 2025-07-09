import glob
import os
from io import BytesIO
from pathlib import Path
from typing import Dict, Generator, Union

import httpx
import pydicom

from pyorthanc import AsyncOrthanc, Orthanc


def upload(client: Orthanc, path_or_ds: Union[str, Path, pydicom.Dataset], recursive: bool = False) -> Union[Dict, httpx.Response]:
    """Upload a DICOM file or dataset to Orthanc synchronously

    Parameters
    ----------
    client : Orthanc
        The Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file, directory, zip file or a pydicom Dataset object
    recursive : bool
        When `path_or_ds` is a directory, whether to upload recursively all the DICOM files in the directory
    """
    if (isinstance(path_or_ds, str) or isinstance(path_or_ds, Path)) and os.path.isdir(path_or_ds):
        for dicom_bytes in _prepare_data_directory(path_or_ds, recursive=recursive):
            client.post_instances(dicom_bytes)

    else:
        dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

        return client.post_instances(dicom_bytes)


async def async_upload(client: AsyncOrthanc, path_or_ds: Union[str, Path, pydicom.Dataset]) -> Union[Dict, httpx.Response]:
    """Upload a DICOM file or dataset to Orthanc asynchronously

    Parameters
    ----------
    client : AsyncOrthanc
        The async Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file, zip file or a pydicom Dataset object
    """
    dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

    return await client.post_instances(dicom_bytes)


def _prepare_data_from_ds_or_file(path_or_ds: Union[str, Path, pydicom.Dataset]) -> bytes:
    # Convert dataset to bytes if needed
    if isinstance(path_or_ds, str) or isinstance(path_or_ds, Path):
        with open(path_or_ds, 'rb') as f:
            dicom_bytes = f.read()
    elif isinstance(path_or_ds, pydicom.Dataset):
        buffer = BytesIO()
        path_or_ds.save_as(buffer)
        dicom_bytes = buffer.getvalue()
    else:
        raise TypeError("path_or_ds must be either a file path or pydicom Dataset")

    return dicom_bytes


def _prepare_data_directory(directory: str, recursive: bool) -> Generator[bytes, None, None]:
    filepaths = glob.glob(os.path.join(directory, '*.dcm'))
    filepaths += glob.glob(os.path.join(directory, '*.DCM'))
    filepaths += glob.glob(os.path.join(directory, '*.dcm.gz'))
    filepaths += glob.glob(os.path.join(directory, '*.DCM.gz'))

    if recursive is True:
        filepaths += glob.glob(os.path.join(directory, '**', '*.dcm'), recursive=recursive)
        filepaths += glob.glob(os.path.join(directory, '**', '*.DCM'), recursive=recursive)
        filepaths += glob.glob(os.path.join(directory, '**', '*.dcm.gz'), recursive=recursive)
        filepaths += glob.glob(os.path.join(directory, '**', '*.DCM.gz'), recursive=recursive)

    filepaths = set(filepaths)

    for filepath in filepaths:
        yield _prepare_data_from_ds_or_file(filepath)
