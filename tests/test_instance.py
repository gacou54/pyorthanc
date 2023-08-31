from datetime import datetime

import pydicom
import pytest

from pyorthanc import errors
from .conftest import LABEL_INSTANCE
from .data import a_series, an_instance

EXPECTED_DATE = datetime(
    year=2010,
    month=3,
    day=1,
    hour=17,
    minute=1,
    second=55
)


def test_attributes(instance):
    assert instance.get_main_information().keys() == an_instance.INFORMATION.keys()

    assert instance.uid == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']
    assert type(instance.file_size) == int
    assert instance.creation_date == EXPECTED_DATE
    assert instance.labels == [LABEL_INSTANCE]
    assert instance.series_identifier == a_series.IDENTIFIER
    assert instance.image_orientation_patient == [1, 0, 0, 0, 1, 0]
    assert instance.image_position_patient == [-223.9880065918, -158.08148193359, -117.78499603271]
    assert instance.instance_number == int(an_instance.INFORMATION['MainDicomTags']['InstanceNumber'])
    assert instance.number_of_frames == 75

    assert '0008,0012' in instance.tags.keys()
    assert 'Value' in instance.tags['0008,0012'].keys()
    assert str(instance) == f'Instance({an_instance.IDENTIFIER})'

    for absent_attribute in ['acquisition_number', 'image_index', 'image_comments', 'temporal_position_identifier']:
        with pytest.raises(errors.TagDoesNotExistError):
            getattr(instance, absent_attribute)


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


def test_pydicom(instance):
    result = instance.get_pydicom()

    assert isinstance(result, pydicom.FileDataset)
    assert result.SOPInstanceUID == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']


@pytest.mark.parametrize('label', ['a_label'])
def test_label(instance, label):
    instance.add_label(label)
    assert label in instance.labels

    instance.remove_label(label)
    assert label not in instance.labels
