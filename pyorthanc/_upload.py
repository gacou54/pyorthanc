import glob
import os
from io import BytesIO
from pathlib import Path
from typing import Dict, Generator, Union

import httpx
import pydicom

from pyorthanc import AsyncOrthanc, Orthanc
from pyorthanc.util import _make_orthanc_id, to_orthanc_study_id, to_orthanc_series_id, to_orthanc_patient_id


def upload(client: Orthanc, path_or_ds: Union[str, Path, pydicom.Dataset], recursive: bool = False, check_before_upload: bool = False) -> Union[Dict, httpx.Response]:
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
    if (isinstance(path_or_ds, str) or isinstance(path_or_ds, Path)) and os.path.isdir(path_or_ds):
        for dicom_bytes in _prepare_data_directory(path_or_ds, recursive=recursive):
            client.post_instances(dicom_bytes)

    else:
        dicom_bytes = _prepare_data_from_ds_or_file(path_or_ds)

        if check_before_upload:
            data_in_orthanc, return_message = _is_data_already_in_orthanc(client, dicom_bytes)
            if data_in_orthanc:
                return return_message

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


def _is_data_already_in_orthanc(client: Orthanc, dicom_bytes):
    dicom_file_like = BytesIO(dicom_bytes)
    ds = pydicom.dcmread(dicom_file_like)
    orthanc_id = _make_orthanc_id_from_ds(ds)

    try:
        info = client.get_instances_id_metadata(id_=orthanc_id)

        return True, _make_already_stored_return_message(ds)
    except httpx.HTTPError as e:
        return False, ''


def _make_orthanc_id_from_ds(ds: pydicom.Dataset):
    return _make_orthanc_id(patient_id=ds.PatientID, study_uid=ds.StudyInstanceUID, series_uid=ds.SeriesInstanceUID,
                            instance_uid=ds.SOPInstanceUID)


def _make_already_stored_return_message(ds):
    instance_id = _make_orthanc_id_from_ds(ds)

    data = {'ID': instance_id,
            'ParentPatient': to_orthanc_patient_id(ds.PatientID),
            'ParentSeries': to_orthanc_series_id(ds.PatientID, ds.StudyInstanceUID, ds.SeriesInstanceUID),
            'ParentStudy': to_orthanc_study_id(ds.PatientID, ds.StudyInstanceUID),
            'Path': f'/instances/{instance_id}',
            'Status': 'AlreadyStored'}

    return data
