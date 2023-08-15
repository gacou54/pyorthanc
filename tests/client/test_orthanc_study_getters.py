import os
import unittest
import zipfile

import httpx

from pyorthanc import Orthanc
from tests.data import a_study
from tests.setup_server import ORTHANC_1, clear_data, setup_data


class TestOrthancStudyGetters(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_patient_in_orthanc_server(self):
        setup_data(ORTHANC_1)

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

        result = self.orthanc.get_studies_id(a_study.IDENTIFIER)

        self.assertIsInstance(result, dict)
        self.assertDictEqual(
            {key: value.sort() if type(value) == list else value for key, value in result.items() if key not in keys_to_exclude},
            {key: value.sort() if type(value) == list else value for key, value in a_study.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenOrthancWithoutPatient_whenGettingStudies_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyZip_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_studies_id_archive(a_study.IDENTIFIER)

        self.assertIsInstance(result, bytes)
        with open(a_study.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_study.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_study.ZIP_FILE_PATH)

    def test_givenOrthancWithoutPatient_whenGettingStudyZip_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id_archive(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstances_thenResultIsAListOfStudyInstanceInformation(self):
        self.given_patient_in_orthanc_server()
        keys_to_exclude = {'FileUuid', 'FileSize'}  # Removing keys that are never the same

        result = self.orthanc.get_studies_id_instances(a_study.IDENTIFIER)

        self.assertIsInstance(result, list)
        result = [{key: value for key, value in i.items() if key not in keys_to_exclude} for i in result]
        expected = [{key: value for key, value in i.items() if key not in keys_to_exclude} for i in a_study.INSTANCES]
        self.assertCountEqual(result, expected)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstances_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id_instances(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTags_thenResultIsADictOfStudyInstancesTags(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER)

        for instance_identifier, instance in result.items():
            for expected_key in a_study.INSTANCE_TAGS[instance_identifier]:
                self.assertIn(expected_key, instance)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTags_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER)
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTagsInSimplifiedVersion_thenResultIsADictOfPatientInstancesTagsInSimplifiedVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER, params={'simplify': True})

        for instance_identifier, instance in result.items():
            for expected_key in a_study.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION[instance_identifier]:
                self.assertIn(expected_key, instance)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTagsInSimplifiedVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER, params={'simplify': True})
        )

    def test_givenOrthancWithPatient_whenGettingStudyInstancesTagsInShorterVersion_thenResultIsADictOfPatientInstancesTagsInShorterVersion(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER, params={'short': True})

        self.assertEqual(result, a_study.INSTANCE_TAGS_IN_SHORTER_VERSION)

    def test_givenOrthancWithoutPatient_whenGettingStudyInstancesTagsInShorterVersion_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.get_studies_id_instances_tags(a_study.IDENTIFIER, params={'short': True})
        )
