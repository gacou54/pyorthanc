import glob
import os
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

import httpx2
import pydicom
from pydicom.errors import InvalidDicomError

from pyorthanc import AsyncOrthanc, Instance, Orthanc
from pyorthanc.util import ensure_non_raw_response, to_orthanc_instance_id_from_ds


def upload(
        client: Orthanc,
        path_or_ds: Union[str, Path, pydicom.Dataset],
        recursive: bool = False,
        check_before_upload: bool = False,
        force: bool = False) -> List[Instance]:
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
    force : bool
        Only used with `check_before_upload=True`. Read the files with `pydicom.dcmread(..., force=True)` to check
        files that are not valid DICOM Part 10 files (e.g. a file without the 128-byte preamble and the "DICM" prefix).
        Without it, these files are always uploaded. Orthanc accepts them in both cases.

    Returns
    -------
    List[Instance]
        The uploaded instances (and the instances that were already in Orthanc when `check_before_upload=True`)
    """
    client = ensure_non_raw_response(client)

    instances = []

    for dicom_bytes in _generate_dicom_bytes(path_or_ds, recursive=recursive):
        if check_before_upload:
            orthanc_id = _get_orthanc_instance_id(dicom_bytes, force)

            if orthanc_id is not None and _is_instance_in_orthanc(client, orthanc_id):
                instances.append(Instance(orthanc_id, client))
                continue

        result = client.post_instances(dicom_bytes)
        instances += [Instance(i['ID'], client) for i in _to_list(result)]

    return instances


async def async_upload(
        client: AsyncOrthanc,
        path_or_ds: Union[str, Path, pydicom.Dataset],
        recursive: bool = False,
        check_before_upload: bool = False,
        force: bool = False) -> List[str]:
    """Upload a DICOM file or dataset to Orthanc asynchronously

    Parameters
    ----------
    client : AsyncOrthanc
        The async Orthanc client to use for upload
    path_or_ds : Union[str, Path, pydicom.Dataset]
        Either a path to a DICOM file, directory, zip file or a pydicom Dataset object
    recursive : bool
        When `path_or_ds` is a directory, whether to upload recursively all the DICOM files in the directory
    check_before_upload : bool
        Verify if data is already in Orthanc before sending it. It verifies if a file is stored, there is no file comparison.
    force : bool
        Only used with `check_before_upload=True`. Read the files with `pydicom.dcmread(..., force=True)` to check
        files that are not valid DICOM Part 10 files (e.g. a file without the 128-byte preamble and the "DICM" prefix).
        Without it, these files are always uploaded. Orthanc accepts them in both cases.

    Returns
    -------
    List[str]
        The Orthanc identifiers of the uploaded instances (and of the instances that were already in Orthanc
        when `check_before_upload=True`). Use them with a synchronous client, e.g. `Instance(id_, Orthanc(...))`,
        since the resource classes do not support `AsyncOrthanc`.
    """
    client = ensure_non_raw_response(client)

    instance_ids = []

    for dicom_bytes in _generate_dicom_bytes(path_or_ds, recursive=recursive):
        if check_before_upload:
            orthanc_id = _get_orthanc_instance_id(dicom_bytes, force)

            if orthanc_id is not None and await _async_is_instance_in_orthanc(client, orthanc_id):
                instance_ids.append(orthanc_id)
                continue

        result = await client.post_instances(dicom_bytes)
        instance_ids += [i['ID'] for i in _to_list(result)]

    return instance_ids


def _generate_dicom_bytes(path_or_ds: Union[str, Path, pydicom.Dataset], recursive: bool) -> Generator[bytes, None, None]:
    # If path_or_ds is a directory, upload all the DICOM files in the directory.
    if isinstance(path_or_ds, (str, Path)) and os.path.isdir(path_or_ds):
        yield from _generate_dicom_bytes_from_directory(path_or_ds, recursive=recursive)

    # If path_or_ds is a DICOM file, zip file or a pydicom Dataset, upload it.
    else:
        yield _prepare_data_from_ds_or_file(path_or_ds)


def _to_list(result: Union[Dict, List[Dict]]) -> List[Dict]:
    # When a zip is uploaded, result is a list of instances (empty if the zip contained no DICOM file).
    return result if isinstance(result, list) else [result]


def _get_orthanc_instance_id(dicom_bytes: bytes, force: bool) -> Optional[str]:
    """Orthanc identifier of the instance in `dicom_bytes`, or None if it cannot be computed (zip file, missing tags...)"""
    if zipfile.is_zipfile(BytesIO(dicom_bytes)):
        return None  # Otherwise, `force=True` would make pydicom "read" the zip file as a dataset

    try:
        ds = pydicom.dcmread(BytesIO(dicom_bytes), force=force, stop_before_pixels=True)
        return to_orthanc_instance_id_from_ds(ds)

    except (InvalidDicomError, AttributeError, ValueError, EOFError, OSError):
        # Not a valid DICOM file, or the identifying tags are missing. The data will be uploaded.
        return None


def _is_instance_in_orthanc(client: Orthanc, orthanc_id: str) -> bool:
    try:
        # Attempt to get metadata to verify if data is already in Orthanc.
        client.get_instances_id_metadata(id_=orthanc_id)
        return True

    except httpx2.HTTPError:
        return False


async def _async_is_instance_in_orthanc(client: AsyncOrthanc, orthanc_id: str) -> bool:
    try:
        # Attempt to get metadata to verify if data is already in Orthanc.
        await client.get_instances_id_metadata(id_=orthanc_id)
        return True

    except httpx2.HTTPError:
        return False


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
