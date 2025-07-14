import glob
import os
from io import BytesIO
from pathlib import Path
from typing import Dict, Generator, List, Tuple, Union

import httpx
import pydicom
from pydicom.errors import InvalidDicomError

from pyorthanc import AsyncOrthanc, Instance, Orthanc
from pyorthanc.util import ensure_non_raw_response, to_orthanc_instance_id_from_ds


def upload(
        client: Orthanc,
        path_or_ds: Union[str, Path, pydicom.Dataset],
        recursive: bool = False,
        check_before_upload: bool = False) -> List[Instance]:
    """Upload a DICOM file or dataset to Orthanc synchronously

    Parameters
    ----------
    client : Orthanc
        The Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file, directory, zip file or a pydicom Dataset object
    recursive : bool
        When `path_or_ds` is a directory, whether to upload recursively all the DICOM files in the directory
    check_before_upload : bool
         Verify if data is already in Orthanc before sending it. It verifies if a file is stored, there is no file comparison.
    """
    client = ensure_non_raw_response(client)

    instances = []

    # If path_or_ds is a directory, upload all the DICOM files in the directory.
    if (isinstance(path_or_ds, str) or isinstance(path_or_ds, Path)) and os.path.isdir(path_or_ds):
        for dicom_bytes in _generate_dicom_bytes_from_directory(path_or_ds, recursive=recursive):
            if check_before_upload:
                data_is_in_orthanc, instance = _is_data_already_in_orthanc(client, dicom_bytes)

                # If data is already in Orthanc, skip uploading it and go to the next file.
                if data_is_in_orthanc:
                    instances.append(instance)
                    continue

            result = client.post_instances(dicom_bytes)
            instance = Instance(result['ID'], client)
            instances.append(instance)

    # If path_or_ds is a DICOM file, zip file or a pydicom Dataset, upload it.
    else:
        dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

        if check_before_upload:
            data_in_orthanc, instance = _is_data_already_in_orthanc(client, dicom_bytes)
            # If data is already in Orthanc, returns the instance directly.
            if data_in_orthanc:
                instances.append(instance)
                return instances

        result = client.post_instances(dicom_bytes)

        # When a zip is uploaded, result can be a list of instances if the zip contained multiple DICOM files.
        if isinstance(result, list):
            instances += [Instance(i['ID'], client) for i in result]
        else:
            instance = Instance(result['ID'], client)
            instances.append(instance)

    return instances


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
        raise TypeError('path_or_ds must be either a file path or pydicom Dataset')

    return dicom_bytes


def _generate_dicom_bytes_from_directory(directory: str, recursive: bool) -> Generator[bytes, None, None]:
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


def _is_data_already_in_orthanc(client: Orthanc, dicom_bytes: bytes) -> Tuple[bool, Union[Instance, None]]:
    try:
        dicom_file_like = BytesIO(dicom_bytes)
        ds = pydicom.dcmread(dicom_file_like)
        orthanc_id = to_orthanc_instance_id_from_ds(ds)
    except InvalidDicomError:
        # If the file is not a valid DICOM file, likely it is a zip file. It will be uploaded.
        return False, None

    try:
        # Attempt to get metadata to verify if data is already in Orthanc.
        client.get_instances_id_metadata(id_=orthanc_id)
        return True, Instance(orthanc_id, client)

    except httpx.HTTPError:
        return False, None
