import os
import unittest
import warnings
import zipfile
from typing import Dict

import httpx

from pyorthanc import Orthanc
from tests.data import a_patient
from tests.setup_server import ORTHANC_1, clear_data, add_data


class TestOrthancPatientGetters(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_patient_in_orthanc_server(self):
        add_data(ORTHANC_1)

    def test_givenOrthancWithPatient_whenGettingPatients_thenResultIsANonEmptyListOfPatientIdentifier(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertIn(a_patient.IDENTIFIER, result)

    def test_givenOrthancWithoutPatient_whenGettingPatients_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithPatient_whenGettingPatientInformation_thenResultIsADictionaryOfPatientInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patients_id(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.INFORMATION.items() if key not in keys_to_remove}
        self.assertDictEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_archive(a_patient.IDENTIFIER)

        self.assertIsInstance(result, bytes)
        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingPatientZip_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_archive(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstances_thenResultIsAListOfPatientInstanceInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = {'FileUuid'}  # Removing keys that are never the same

        result = self.orthanc.get_patients_id_instances(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in a_patient.INSTANCES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_instances(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTags_thenResultIsADictOfPatientInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER)

        for instance_identifier, instance in result.items():
            for expected_key in a_patient.INSTANCE_TAGS[instance_identifier]:
                self.assertIn(expected_key, instance)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER, params={'simplify': True})

        for instance_identifier, instance in result.items():
            for expected_key in a_patient.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION[instance_identifier]:
                self.assertIn(expected_key, instance)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER, params={'simplify': True})
        )

    def test_givenOrthancWithPatient_whenGettingPatientInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER, params={'short': True})

        self.assertEqual(result, a_patient.INSTANCE_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_instances_tags(a_patient.IDENTIFIER, params={'short': True})
        )

    def test_givenOrthancWithPatient_whenGettingPatientArchive_thenResultIsBytesOfAValidZipFileOfPatientArchive(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_archive(a_patient.IDENTIFIER)

        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingPatientArchive_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_archive(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientModule_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_module(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.MODULE)

    def test_givenOrthancWithoutPatient_whenGettingPatientModule_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_module(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientModuleInSimplifiedVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_module(a_patient.IDENTIFIER, params={'simplify': True})

        self.assertEqual(result, a_patient.MODULE_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientModuleInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_module(a_patient.IDENTIFIER, params={'simplify': True})
        )

    def test_givenOrthancWithPatient_whenGettingPatientModuleInShorterVersion_thenResultIsExpectedTagInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_module(a_patient.IDENTIFIER, params={'short': True})

        self.assertEqual(result, a_patient.MODULE_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientModuleInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_module(a_patient.IDENTIFIER, params={'short': True})
        )

    def test_givenOrthancWithUnprotectedPatient_whenGettingIfPatientIsProtected_thenResultIsFalse(self):
        warnings.warn('Cannot set Patient to unprotected (not working with the generated Orthanc client) -- skipping test')
        # self.given_patient_in_orthanc_server()
        # self.orthanc._put(route=f'{self.orthanc.url}/patients/{a_patient.IDENTIFIER}/protected', json=0)

        # result = self.orthanc.get_patients_id_protected(a_patient.IDENTIFIER)

        # self.assertEqual(result, '0')

    def test_givenOrthancWithProtectedPatient_whenGettingIfPatientIsProtected_thenResultIsTrue(self):
        warnings.warn('Cannot set Patient to protected (not working with the generated Orthanc client) -- skipping test')
        # self.given_patient_in_orthanc_server()
        # self.orthanc.put_patients_id_protected(a_patient.IDENTIFIER)
        #
        # result = self.orthanc.get_patients_id_protected(a_patient.IDENTIFIER)
        #
        # self.assertTrue(result)

    def test_givenOrthancWithAPatient_whenGettingPatientSeries_thenResultIsAListOfPatientSeriesMainInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patients_id_series(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_remove} for i in a_patient.SERIES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientSeries_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_series(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTags_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER)

        self.assertEqual(result, a_patient.SHARED_TAGS)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTags_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInSimplifiedVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER, params={'simplify': True})

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER, params={'simplify': True})
        )

    def test_givenOrthancWithAPatient_whenGettingPatientSharedTagsInShorterVersion_thenResultIsExpectedTagsInExpectedFormat(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER, params={'short': True})

        self.assertEqual(result, a_patient.SHARED_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingPatientSharedTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_shared_tags(a_patient.IDENTIFIER, params={'short': True})
        )

    def test_givenOrthancWithPatient_whenGettingPatientStatistics_thenResultIsExpectedPatientStatistics(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['DiskSize', 'UncompressedSize', 'DiskSizeMB', 'UncompressedSizeMB']  # Removing keys that are never the same

        result = self.orthanc.get_patients_id_statistics(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        result = {key: value for key, value in result.items() if key not in keys_to_remove}
        expected = {key: value for key, value in a_patient.STATISTICS.items() if key not in keys_to_remove}
        self.assertDictEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientStatistics_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_statistics(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingPatientStudiesInformation_thenResultIsExpectedPatientStudiesInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_remove = ['LastUpdate']  # Removing keys that are never the same

        result = self.orthanc.get_patients_id_studies(a_patient.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [self._sort_dictionary_element({key: value for key, value in i.items() if key not in keys_to_remove}) for i in result]
        expected = [self._sort_dictionary_element({key: value for key, value in i.items() if key not in keys_to_remove}) for i in a_patient.STUDIES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingPatientStudiesInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_patients_id_studies(a_patient.IDENTIFIER)
        )

    def _sort_dictionary_element(self, dictionary: Dict) -> Dict:
        for key, value in dictionary.items():
            if type(value) == list:
                dictionary[key] = value.sort()

            elif type(value) == dict:
                dictionary[key] = self._sort_dictionary_element(value)

        return dictionary
