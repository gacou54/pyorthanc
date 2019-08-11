# coding: utf-8
# author: gabriel couture
import os
import unittest
import zipfile

import requests

from pyorthanc import Orthanc
from tests.integration import setup_server
from tests.integration.data import a_patient


class TestOrthancPatientGetter(unittest.TestCase):

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

    def given_patient_in_orthanc_server(self):
        setup_server.setup_data()

    def test_givenOrthancWithData_whenGettingPatients_thenResultIsANonEmptyListOfPatientIdentifier(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)
        for patient_identifier in result:
            self.assertIn(patient_identifier, [a_patient.IDENTIFIER])

    def test_givenOrthancWithoutData_whenGettingPatients_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithData_whenGettingPatientInformation_thenResultIsADictionaryOfPatientInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']

        result = self.orthanc.get_patient_information(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        # Removing a key that is never the same
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.INFORMATION.items() if key not in keys_to_remove}
        self.assertDictEqual(result, expected)

    def test_givenOrthancWithoutData_whenGettingPatientInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_information(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_zip(a_patient.IDENTIFIER)

        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithData_whenGettingPatientZip_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_zip(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstances_thenResultIsAListOfPatientInstanceInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['FileUuid', 'FileSize']

        result = self.orthanc.get_patient_instances(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        # Removing a key that is never the same
        result = [{key: value for key, value in elem.items() if key not in keys_to_remove} for elem in result]
        expected = [{key: value for key, value in elem.items() if key not in keys_to_remove} for elem in a_patient.INSTANCES]
        self.assertEqual(result, expected)

    def test_givenOrthancWithoutData_whenGettingPatientInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTags_thenResultIsADictOfPatientInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS)

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_simplified_version(
                a_patient.IDENTIFIER
            )
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_shorter_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientArchive_thenResultIsBytesOfAValidZipFileOfPatientArchive(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_archive(a_patient.IDENTIFIER)

        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithoutData_whenGettingPatientArchive_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_archive(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModule_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE)

    def test_givenOrthancWithoutData_whenGettingPatientModule_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModuleInSimplifiedVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientModuleInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module_in_simplified_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModuleInShorterVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientModuleInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module_in_shorter_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithUnprotectedPatient_whenGettingIfPatientIsProtected_thenResultIsFalse(self):
        self.given_patient_in_orthanc_server()
        self.orthanc.set_patient_to_not_protected(a_patient.IDENTIFIER)

        result = self.orthanc.get_if_patient_is_protected(a_patient.IDENTIFIER)

        self.assertFalse(result)

    def test_givenOrthancWithProtectedPatient_whenGettingIfPatientIsProtected_thenResultIsTrue(self):
        self.given_patient_in_orthanc_server()
        self.orthanc.set_patient_to_protected(a_patient.IDENTIFIER)

        result = self.orthanc.get_if_patient_is_protected(a_patient.IDENTIFIER)

        self.assertTrue(result)

    def test_givenOrthancWithAPatient_whenGettingPatientSeries_thenResultIsAListOfPatientSeriesMainInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']

        result = self.orthanc.get_patient_series(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        # Removing a key that is never the same
        result = [{key: value for key, value in elem.items() if key not in keys_to_remove} for elem in result]
        expected = [{key: value for key, value in elem.items() if key not in keys_to_remove} for elem in a_patient.SERIES]
        self.assertEqual(result, expected)

    def test_givenOrthancWithoutData_whenGettingPatientSeries_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_series(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTags_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS)

    def test_givenOrthancWithoutData_whenGettingPatientSharedTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInSimplifiedVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientSharedTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags_in_simplified_version(a_patient.IDENTIFIER)
            )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInShorterVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutData_whenGettingPatientSharedTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags_in_shorter_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientStatistics_thenResultIsExpectedPatientStatistics(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['DiskSize', 'UncompressedSize']

        result = self.orthanc.get_patient_statistics(a_patient.IDENTIFIER)

        # Removing keys that are not always the same
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.STATISTICS.items() if key not in keys_to_remove}
        self.assertEqual(result, expected)

    def test_givenOrthancWithPatient_whenGettingPatientStatistics_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_statistics(a_patient.IDENTIFIER)
        )
