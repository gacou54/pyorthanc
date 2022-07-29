from datetime import datetime

import pytest

from pyorthanc import Orthanc, Instance
from .data import an_instance
from .setup_server import ORTHANC_1, setup_data, clear_data

EXPECTED_DATE = datetime(
    year=2010,
    month=3,
    day=1,
    hour=17,
    minute=1,
    second=55
)


@pytest.fixture
def instance():
    setup_data(ORTHANC_1)

    client = Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)
    yield Instance(client=client, instance_id=client.get_instances()[0])

    clear_data(ORTHANC_1)


def test_attributes(instance):
    assert instance.get_main_information().keys() == an_instance.INFORMATION.keys()

    assert instance.uid == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']
    assert type(instance.file_size) == int
    assert instance.creation_date == EXPECTED_DATE
    assert instance.series_id == an_instance.SERIES_ID

    assert '0008,0012' in instance.tags.keys()
    assert 'Value' in instance.tags['0008,0012'].keys()


def test_get_tag_content(instance):
    tag, expected_content = 'ManufacturerModelName', 'Pinnacle3'
    assert instance.get_content_by_tag(tag) == expected_content

    tag, expected_content = '0008-1090', 'Pinnacle3'
    assert instance.get_content_by_tag(tag) == expected_content

    group_element = 'ReferencedStudySequence/0/ReferencedSOPClassUID'
    expected_content = '1.2.840.10008.3.1.2.3.2'
    assert instance.get_content_by_tag(group_element) == expected_content

    group_element = '0008-1110/0/0008-1150'
    expected_content = '1.2.840.10008.3.1.2.3.2'
    assert instance.get_content_by_tag(group_element) == expected_content


def test_anonymize(instance):
    anonymized_instance = instance.anonymize(remove=['InstanceCreationDate'])

    assert type(anonymized_instance) == bytes
