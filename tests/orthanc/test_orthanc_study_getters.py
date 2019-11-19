# coding: utf-8
# author: gabriel couture
import os
import unittest
import zipfile

from pyorthanc import Orthanc
from pyorthanc.exceptions import HTTPError
from tests import setup_server
from tests.data import a_study


class TestOrthancStudyGetters(unittest.TestCase):

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

    def test_givenOrthancWithPatient_whenGettingStudies_thenResultIsANonEmptyListOfStudyIdentifiers(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_studies()

        self.assertIsInstance(result, list)
        self.assertIn(a_study.IDENTIFIER, result)

    def test_givenOrthancWithoutPatient_whenGettingStudies_thenResultIsAnEmptyList(self):
        result = self.orthanc.get_studies()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_givenOrthancWithAPatient_whenGettingStudies_thenResultIsExpectedStudyInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_exclude = {'LastUpdate'}

        result = self.orthanc.get_study_information(a_study.IDENTIFIER)

        self.assertIsInstance(result, dict)
        self.assertDictEqual(
            {key: value.sort() if type(value) == list else value for key, value in result.items() if key not in keys_to_exclude},
            {key: value.sort() if type(value) == list else value for key, value in a_study.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenOrthancWithoutPatient_whenGettingStudies_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_information(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_study_zip_file(a_study.IDENTIFIER)

        self.assertIsInstance(result, bytes)
        with open(a_study.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_study.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_study.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingStudyZip_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_zip_file(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstances_thenResultIsAListOfStudyInstanceInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_exclude = {'FileUuid', 'FileSize'}  # Removing keys that are never the same

        result = self.orthanc.get_study_instances(a_study.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_exclude} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_exclude} for i in a_study.INSTANCES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_instances(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTags_thenResultIsADictOfStudyInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_study_instances_tags(a_study.IDENTIFIER)

        self.assertEqual(result, a_study.INSTANCE_TAGS)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_instances_tags(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_study_instances_tags_in_simplified_version(a_study.IDENTIFIER)

        self.assertEqual(result, a_study.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_instances_tags_in_simplified_version(
                a_study.IDENTIFIER
            )
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_study_instances_tags_in_shorter_version(a_study.IDENTIFIER)

        self.assertEqual(result, a_study.INSTANCE_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_study_instances_tags_in_shorter_version(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyArchive_thenResultIsBytesOfAValidZipFileOfStudyArchive(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patient_archive(a_study.IDENTIFIER)

        with open(a_study.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_study.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_study.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingStudyArchive_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.get_patient_archive(a_study.IDENTIFIER)
        )
