from io import BytesIO
from pathlib import Path
from typing import Dict, List, Union

import httpx
import pydicom

from pyorthanc import AsyncOrthanc, Orthanc


def upload(client: Orthanc, path_or_ds: Union[str, Path, pydicom.Dataset]) -> Union[Dict, httpx.Response]:
    """Upload a DICOM file or dataset to Orthanc synchronously

    Parameters
    ----------
    client : Orthanc
        The Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file or a pydicom Dataset object
    """
    dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

    return client.post_instances(dicom_bytes)


async def async_upload(client: AsyncOrthanc, path_or_ds: Union[str, Path, pydicom.Dataset]) -> Union[Dict, httpx.Response]:
    """Upload a DICOM file or dataset to Orthanc asynchronously

    Parameters
    ----------
    client : AsyncOrthanc
        The async Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file or a pydicom Dataset object
    """
    dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

    return await client.post_instances()


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
