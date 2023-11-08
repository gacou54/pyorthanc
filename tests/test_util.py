from datetime import datetime

import pydicom
import pytest

from pyorthanc import AsyncOrthanc, Orthanc, util
from .data import a_patient, a_series, a_study, an_instance


def test_async_to_sync(async_client):
    result = util.async_to_sync(async_client)

    assert isinstance(result, Orthanc)


def test_sync_to_async(client_with_data):
    result = util.sync_to_async(client_with_data)

    assert isinstance(result, AsyncOrthanc)


@pytest.mark.parametrize('date_str, time_str, expected', [
    ('20100301', '170155', datetime(year=2010, month=3, day=1, hour=17, minute=1, second=55)),
    ('20100301', 'bad_time', datetime(year=2010, month=3, day=1)),
    ('20100301', None, datetime(year=2010, month=3, day=1)),
    ('bad_date', None, None),
])
def test_make_datetime_from_dicom_date(date_str, time_str, expected):
    result = util.make_datetime_from_dicom_date(date_str, time_str)

    assert result == expected


def test_get_pydicom(client_with_data):
    result = util.get_pydicom(client_with_data, an_instance.IDENTIFIER)

    assert isinstance(result, pydicom.FileDataset)
    assert result.SOPInstanceUID == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']


@pytest.mark.parametrize('return_raw_response', [True, False])
def test_ensure_non_raw_response(client, return_raw_response):
    client.return_raw_response = return_raw_response

    new_client = util.ensure_non_raw_response(client)

    assert not new_client.return_raw_response
    assert client.return_raw_response == return_raw_response


PATIENT_ID = '03HDQ000'
STUDY_UID = '1.2.840.113619.2.55.3.671782272.419.1266452812.128'
SERIES_UID = '1.2.840.113619.2.55.3.671782272.419.1266452812.128'
INSTANCE_UID = '2.16.840.1.113669.2.931128.981194414.20100301170155.668389'

EXPECTED_PATIENT_ID = 'e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8'
EXPECTED_STUDY_ID = '118bc493-b3b3172a-082119bd-f6802ec3-81695613'
EXPECTED_SERIES_ID = 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06'
EXPECTED_INSTANCE_ID = '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9'


def test_to_orthanc_patient_id():
    result = util.to_orthanc_patient_id(a_patient.ID)

    assert result == a_patient.IDENTIFIER


def test_to_orthanc_study_id():
    result = util.to_orthanc_study_id(a_patient.ID, a_study.UID)

    assert result == a_study.IDENTIFIER


def test_to_orthanc_series_id():
    result = util.to_orthanc_series_id(a_patient.ID, a_study.UID, a_series.UID)

    assert result == a_series.IDENTIFIER


def test_to_orthanc_instance_id():
    result = util.to_orthanc_instance_id(a_patient.ID, a_study.UID, a_series.UID, an_instance.UID)

    assert result == an_instance.IDENTIFIER
