# coding: utf-8
# author: Gabriel Couture
import unittest
from datetime import datetime

from pyorthanc import Orthanc
from pyorthanc.util import Instance
from tests import setup_server
from tests.data import a_instance


class TestInstance(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global orthanc_subprocess
        orthanc_subprocess = setup_server.setup_orthanc_server()

    @classmethod
    def tearDownClass(cls) -> None:
        global orthanc_subprocess
        setup_server.stop_orthanc_server_and_remove_data_directory(orthanc_subprocess)
        del orthanc_subprocess

    def setUp(self) -> None:
        setup_server.setup_data()

        self.instance = Instance(
            a_instance.IDENTIFIER,
            Orthanc(setup_server.ORTHANC_URL)
        )

    def tearDown(self) -> None:
        self.instance = None
        setup_server.clear_data()

    def test_givenAInstance_whenGettingMainInformation_thenResultIsExpectedPatientInformation(self):
        keys_to_exclude = {'LastUpdate', 'FileSize', 'FileUuid'}

        result = self.instance.get_main_information()

        self.assertDictEqual(
            {key: value for key, value in result.items() if key not in keys_to_exclude},
            {key: value for key, value in a_instance.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenAInstance_whenGettingFileSize_thenResultIsAInt(self):
        result = self.instance.get_file_size()

        self.assertIsInstance(result, int)  # The fileSize value depends on the machine where Orthanc run

    def test_givenAInstance_whenGettingCreationDate_thenResultIsExpectedCreationDate(self):
        expected_date = datetime(
            year=2010,
            month=3,
            day=1,
            hour=17,
            minute=1,
            second=55
        )

        result = self.instance.get_creation_date()

        self.assertEqual(result, expected_date)

    def test_givenAInstance_whenGettingParentSeriesIdentifier_thenResultIsExpectedParentSeriesIdentifier(self):
        result = self.instance.get_parent_series_identifier()

        self.assertEqual(result, a_instance.PARENT_SERIES_IDENTIFIER)

    def test_givenAInstanceAndATag_whenGettingTagContent_thenResultIsExpectedContent(self):
        a_tag = 'ManufacturerModelName'
        expected_content = 'Pinnacle3'

        result = self.instance.get_content_by_tag(a_tag)

        self.assertEqual(result, expected_content)

    def test_givenAInstanceAndANumberedDICOMTag_whenGettingTagContent_thenResultIsExpectedContent(self):
        a_tag = '0008-1090'
        expected_content = 'Pinnacle3'

        result = self.instance.get_content_by_tag(a_tag)

        self.assertEqual(result, expected_content)

    def test_givenAInstanceAndAGroupElement_whenGettingGroupElementContent_thenResultIsExpectedContent(self):
        a_group_element = 'ReferencedStudySequence/0/ReferencedSOPClassUID'
        expected_content = '1.2.840.10008.3.1.2.3.2'

        result = self.instance.get_content_by_tag(a_group_element)

        self.assertEqual(result, expected_content)

    def test_givenAInstanceAndAGroupElementWithNumberedDICOMTag_whenGettingGroupElementContent_thenResultIsExpectedContent(self):
        a_group_element = '0008-1110/0/0008-1150'
        expected_content = '1.2.840.10008.3.1.2.3.2'

        result = self.instance.get_content_by_tag(a_group_element)

        self.assertEqual(result, expected_content)
