from datetime import datetime

import pydicom
import pytest

from pyorthanc import Orthanc, AsyncOrthanc, util
from tests.setup_server import ORTHANC_1, setup_data, clear_data
from tests.data import an_instance


@pytest.fixture
def orthanc() -> Orthanc:
    setup_data(ORTHANC_1)

    yield Orthanc(url=ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def async_orthanc() -> AsyncOrthanc:
    return AsyncOrthanc(url=ORTHANC_1.url)


def test_async_to_sync(async_orthanc):
    result = util.async_to_sync(async_orthanc)

    assert isinstance(result, Orthanc)


def test_sync_to_async(orthanc):
    result = util.sync_to_async(orthanc)

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


def test_get_pydicom(orthanc):
    result = util.get_pydicom(orthanc, an_instance.IDENTIFIER)

    assert isinstance(result, pydicom.FileDataset)
    assert result.SOPInstanceUID == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']
