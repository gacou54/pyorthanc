from datetime import datetime

import pydicom
import pytest

from pyorthanc import Orthanc, AsyncOrthanc, util
from .data import an_instance


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
