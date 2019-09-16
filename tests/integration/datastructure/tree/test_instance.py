# coding: utf-8
# author: Gabriel Couture
import unittest
from datetime import datetime

from pyorthanc import Orthanc
from pyorthanc.datastructure import Instance
from tests.integration import setup_server
from tests.integration.data import a_instance


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
