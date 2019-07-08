# coding: utf-8
# author: gabriel couture
import unittest

import requests

from pyorthanc import Orthanc
from tests.integration import setup_server


class TestOrthancInstance(unittest.TestCase):
    A_INSTANCE_IDENTIFIER = '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9'

    A_LIST_OF_INSTANCE_IDENTIFIERS = [
        '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9',
        '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220',
        'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599',
    ]

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
        self.orthanc = Orthanc(setup_server.ORTHANC_URL)

    def tearDown(self) -> None:
        self.orthanc = None
        setup_server.clear_data()

    def given_instances_in_orthanc_server(self):
        setup_server.setup_data()

    def test_givenOrthancWithData_whenGettingInstances_thenResultIsAListOfInstanceIdentifiers(self):
        self.given_instances_in_orthanc_server()

        result = self.orthanc.get_instances()

        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)
        for instance_identifier in result:
            self.assertIn(instance_identifier, TestOrthancInstance.A_LIST_OF_INSTANCE_IDENTIFIERS)

    def test_givenOrthancWithoutData_whenGettingInstances_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_instances()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithData_whenGettingInstanceFirstLevelTags_thenResultIsAListOfFirstLevelDICOMTags(self):
        self.given_instances_in_orthanc_server()

        result = self.orthanc.get_instance_first_level_tags(TestOrthancInstance.A_INSTANCE_IDENTIFIER)

        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)
        for tag in result:
            tag_numbers = tag.split('-')
            self.assertEqual(len(tag_numbers), 2)

            for tag_number in tag_numbers:
                hex(int(tag_number, 16))

    def test_givenOrthancWithoutData_whenGettingInstanceFirstLevelTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_instance_first_level_tags(TestOrthancInstance.A_INSTANCE_IDENTIFIER)
        )
