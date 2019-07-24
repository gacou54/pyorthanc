# coding: utf-8
# author: gabriel couture
import os
import unittest
import zipfile

import requests

from pyorthanc import Orthanc
from tests.integration import setup_server

A_PATIENT_IDENTIFIER = 'e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8'
A_PATIENT_ID = '03HDQ000'
A_PATIENT_NAME = 'MR-R'
A_PATIENT_SEX = 'M'
A_PATIENT_STUDIES = ['118bc493-b3b3172a-082119bd-f6802ec3-81695613']
A_PATIENT_INFORMATION = {
    'ID': A_PATIENT_IDENTIFIER,
    'IsStable': False,
    'LastUpdate': 'THIS_IS_VARIABLE',
    'MainDicomTags': {
        'PatientBirthDate': '',
        'PatientID': A_PATIENT_ID,
        'PatientName': A_PATIENT_NAME,
        'PatientSex': A_PATIENT_SEX
    },
    'Studies': A_PATIENT_STUDIES,
    'Type': 'Patient'
}

A_LIST_OF_INSTANCE_IDENTIFIERS_OF_A_PATIENT = [
    'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599',
    '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220',
    '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9'
]

A_PATIENT_ZIP_FILE_PATH = './tests/integration/data/A_PATIENT_DATA.zip'


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
            self.assertIn(patient_identifier, [A_PATIENT_IDENTIFIER])

    def test_givenOrthancWithoutData_whenGettingPatients_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_patients()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithData_whenGettingPatientInformation_thenResultIsADictionaryOfPatientInformation(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_information(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        # Removing a key that is never the same
        result = {key: value for key, value in result.items() if key != 'LastUpdate'}
        target = {key: value for key, value in A_PATIENT_INFORMATION.items() if key != 'LastUpdate'}
        self.assertDictEqual(result, target)

    def test_givenOrthancWithoutData_whenGettingPatientInformation_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_information(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_zip(A_PATIENT_IDENTIFIER)

        with open(A_PATIENT_ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(A_PATIENT_ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(A_PATIENT_ZIP_FILE_PATH)

    def test_givenOrthancWithData_whenGettingPatientZip_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_zip(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstances_thenResultIsAListOfPatientInstanceInformation(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, list)
        for instance_information in result:
            self.assertIsInstance(instance_information, dict)
            self.assertIn(instance_information['ID'], A_LIST_OF_INSTANCE_IDENTIFIERS_OF_A_PATIENT)

    def test_givenOrthancWithoutData_whenGettingPatientInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTags_thenResultIsADictOfPatientInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for instance_identifier, instance_tags in result.items():
            self.assertIsInstance(instance_tags, dict)

            for tag, tag_content in instance_tags.items():
                for key in tag_content.keys():
                    self.assertIn(key, ('Name', 'Type', 'Value'))

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(
            self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_simplified_version(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for instance_identifier, instance_tags in result.items():
            self.assertIsInstance(instance_tags, dict)

            for tag, tag_content in instance_tags.items():
                self.assertIsInstance(tag, str)
                self.assertIn(type(tag_content), (dict, list, str, type(None)))

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_simplified_version(
                A_PATIENT_IDENTIFIER
            )
        )

    def test_givenOrthancWithData_whenGettingPatientInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_instances_tags_in_shorter_version(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for instance_identifier, instance_tags in result.items():
            self.assertIsInstance(instance_tags, dict)

            for tag, tag_content in instance_tags.items():
                tag_numbers = tag.split(',')
                self.assertEqual(len(tag_numbers), 2)

                for tag_number in tag_numbers:
                    hex(int(tag_number, 16))

                self.assertIn(type(tag_content), (dict, list, str, type(None)))

    def test_givenOrthancWithoutData_whenGettingPatientInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_instances_tags_in_shorter_version(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientArchive_thenResultIsBytesOfAValidZipFileOfPatientArchive(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_archive(A_PATIENT_IDENTIFIER)

        with open(A_PATIENT_ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(A_PATIENT_ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(A_PATIENT_ZIP_FILE_PATH)

    def test_givenOrthancWithoutData_whenGettingPatientArchive_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.exceptions.HTTPError,
            lambda: self.orthanc.get_patient_archive(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModule_thenResultIsADictOfDICOMPatientModuleTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for dicom_tag, tag in result.items():
            self.assertIn('0010,', dicom_tag)
            self.assertIsInstance(tag, dict)

            for key in tag.keys():
                self.assertIn(key, ('Name', 'Type', 'Value'))

    def test_givenOrthancWithoutData_whenGettingPatientModule_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModuleInSimplifiedVersion_thenResultIsADictOfDICOMPatientModuleTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_simplified_version(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for dicom_simplified_tag, tag in result.items():
            self.assertIn('Patient', dicom_simplified_tag)
            self.assertIsInstance(tag, str)

    def test_givenOrthancWithoutData_whenGettingPatientModuleInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module_in_simplified_version(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithData_whenGettingPatientModuleInShorterVersion_thenResultIsADictOfDICOMPatientModuleTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_module_in_shorter_version(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, dict)
        for dicom_tag, tag in result.items():
            self.assertIn('0010,', dicom_tag)
            self.assertIsInstance(tag, str)

    def test_givenOrthancWithoutData_whenGettingPatientModuleInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_module_in_shorter_version(A_PATIENT_IDENTIFIER)
        )

    def test_givenOrthancWithUnprotectedPatient_whenGettingIfPatientIsProtected_thenResultIsFalse(self):
        self.given_patient_in_orthanc_server()
        self.orthanc.set_patient_to_not_protected(A_PATIENT_IDENTIFIER)

        result = self.orthanc.get_if_patient_is_protected(A_PATIENT_IDENTIFIER)

        self.assertFalse(result)

    def test_givenOrthancWithProtectedPatient_whenGettingIfPatientIsProtected_thenResultIsTrue(self):
        self.given_patient_in_orthanc_server()
        self.orthanc.set_patient_to_protected(A_PATIENT_IDENTIFIER)

        result = self.orthanc.get_if_patient_is_protected(A_PATIENT_IDENTIFIER)

        self.assertTrue(result)

    def test_givenOrthancWithAPatient_whenGettingPatientSeries_thenResultIsAListOfPatientSeriesMainInformation(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_series(A_PATIENT_IDENTIFIER)

        self.assertIsInstance(result, list)
        for series in result:
            self.assertIsInstance(series, dict)
            self.assertEqual(series['Type'], 'Series')
            self.assertIn(series['ParentStudy'], A_PATIENT_STUDIES)

    def test_givenOrthancWithoutData_whenGettingPatientSeries_thenRaiseHTTPError(self):
        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.get_patient_series(A_PATIENT_IDENTIFIER)
        )
