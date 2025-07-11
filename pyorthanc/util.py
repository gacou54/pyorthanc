import copy
import hashlib
import re
import warnings
from datetime import datetime
from io import BytesIO
from typing import Optional

import pydicom

from .async_client import AsyncOrthanc
from .client import Orthanc


def delete_queries(client: Orthanc) -> None:
    for query_id in client.get_queries():
        client.delete_queries_id(query_id)


async def async_delete_queries(client: AsyncOrthanc) -> None:
    for query_id in await client.get_queries():
        await client.delete_queries_id(query_id)


def make_datetime_from_dicom_date(date: str, time: str = None) -> Optional[datetime]:
    """Attempt to decode date"""
    try:
        return datetime(
            year=int(date[:4]),
            month=int(date[4:6]),
            day=int(date[6:8]),
            hour=int(time[:2]),
            minute=int(time[2:4]),
            second=int(time[4:6])
        )
    except (ValueError, TypeError):
        try:
            return datetime(
                year=int(date[:4]),
                month=int(date[4:6]),
                day=int(date[6:8]),
            )
        except (ValueError, TypeError):
            return None


def async_to_sync(orthanc: AsyncOrthanc) -> Orthanc:
    sync_orthanc = Orthanc(url=orthanc.url)
    sync_orthanc._auth = orthanc.auth

    return sync_orthanc


def sync_to_async(orthanc: Orthanc) -> AsyncOrthanc:
    async_orthanc = AsyncOrthanc(url=orthanc.url)
    async_orthanc._auth = orthanc.auth

    return async_orthanc


def get_pydicom(orthanc: Orthanc, instance_identifier: str) -> pydicom.FileDataset:
    """Get a pydicom.FileDataset from the instance's Orthanc identifier"""
    dicom_bytes = orthanc.get_instances_id_file(instance_identifier)

    return pydicom.dcmread(BytesIO(dicom_bytes))


def ensure_non_raw_response(client: Orthanc) -> Orthanc:
    if client.return_raw_response:
        warnings.warn(
            'client.return_raw_response is True, which is currently not supported for this class/function. '
            'Will use the client with client.return_raw_response=False'
        )
        client = copy.copy(client)
        client.return_raw_response = False

    return client


def to_orthanc_patient_id(patient_id: str) -> str:
    return _make_orthanc_id(patient_id)


def to_orthanc_study_id(patient_id: str, study_uid: str) -> str:
    return _make_orthanc_id(patient_id, study_uid)


def to_orthanc_series_id(patient_id: str, study_uid: str, series_uid: str) -> str:
    return _make_orthanc_id(patient_id, study_uid, series_uid)


def to_orthanc_instance_id(patient_id: str, study_uid: str, series_uid: str, instance_uid) -> str:
    return _make_orthanc_id(patient_id, study_uid, series_uid, instance_uid)


def to_orthanc_instance_id_from_ds(ds: pydicom.Dataset) -> str:
    return _make_orthanc_id(
        patient_id=ds.PatientID,
        study_uid=ds.StudyInstanceUID,
        series_uid=ds.SeriesInstanceUID,
        instance_uid=ds.SOPInstanceUID
    )


def _make_orthanc_id(patient_id: str, study_uid: str = None, series_uid: str = None, instance_uid: str = None) -> str:
    ids = [patient_id, study_uid, series_uid, instance_uid]

    ids_string = '|'.join([i for i in ids if i is not None])
    uid = hashlib.sha1(ids_string.encode()).hexdigest()

    return re.sub(r'(\S{8})(\S{8})(\S{8})(\S{8})(\S{8})', r'\1-\2-\3-\4-\5', uid)
