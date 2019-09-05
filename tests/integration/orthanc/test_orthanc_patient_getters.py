# coding: utf-8
# author: gabriel couture
import os
import unittest
import zipfile
from typing import Dict

import requests

from pyorthanc import Orthanc
from tests.integration import setup_server
from tests.integration.data import a_patient


class TestOrthancPatientGetters(unittest.TestCase):

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

    def test_givenOrthancWithPatient_whenGettingPatients_thenResultIsANonEmptyListOfPatientIdentifier(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)
        for patient_identifier in result:
            self.assertIn(patient_identifier, [a_patient.IDENTIFIER])

    def test_givenOrthancWithoutPatient_whenGettingPatients_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithPatient_whenGettingPatientInformation_thenResultIsADictionaryOfPatientInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patient_information(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.INFORMATION.items() if key not in keys_to_remove}
        self.assertDictEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_information(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_zip(a_patient.IDENTIFIER)

        self.assertIsInstance(result, bytes)
        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithPatient_whenGettingPatientZip_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_zip(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstances_thenResultIsAListOfPatientInstanceInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['FileUuid']  # Removing keys that are never the same

        result = self.orthanc.get_patient_instances(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in a_patient.INSTANCES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTags_thenResultIsADictOfPatientInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_simplified_version(
                a_patient.IDENTIFIER
            )
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.INSTANCE_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_shorter_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientArchive_thenResultIsBytesOfAValidZipFileOfPatientArchive(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_archive(a_patient.IDENTIFIER)

        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingPatientArchive_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_archive(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientModule_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE)

    def test_givenOrthancWithoutPatient_whenGettingPatientModule_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientModuleInSimplifiedVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientModuleInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module_in_simplified_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientModuleInShorterVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientModuleInShorterVersion_thenRaiseHTTPError(self):
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
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patient_series(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in a_patient.SERIES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientSeries_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_series(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTags_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInSimplifiedVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags_in_simplified_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags_in_simplified_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInShorterVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_shared_tags_in_shorter_version(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_shared_tags_in_shorter_version(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientStatistics_thenResultIsExpectedPatientStatistics(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['DiskSize', 'UncompressedSize']  # Removing keys that are never the same

        result = self.orthanc.get_patient_statistics(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.STATISTICS.items() if key not in keys_to_remove}
        self.assertDictEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientStatistics_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_statistics(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientStudiesInformation_thenResultIsExpectedPatientStudiesInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patient_studies_information(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [self._sort_dictionary_element({key: value for key, value in i.items() if key not in keys_to_remove}) for i in result]
        expected = [self._sort_dictionary_element({key: value for key, value in i.items() if key not in keys_to_remove}) for i in a_patient.STUDIES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientStudiesInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_studies_information(a_patient.IDENTIFIER)
        )

    def _sort_dictionary_element(self, dictionary: Dict) -> Dict:
        for key, value in dictionary.items():
            if type(value) == list:
                dictionary[key] = value.sort()

            elif type(value) == dict:
                dictionary[key] = self._sort_dictionary_element(value)

        return dictionary
