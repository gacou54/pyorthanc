import os
import unittest
import zipfile

import httpx

from pyorthanc import Orthanc
from tests.data import a_patient
from tests.setup_server import ORTHANC_1, clear_data, setup_data


class TestOrthancPatientPosts(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_patient_in_orthanc_server(self):
        setup_data(ORTHANC_1)

    def test_givenOrthancWithAPatient_whenAnonymizeAPatient_thenResultIsIdentifiersOfNewAnonymousPatientAndANewAnonymousPatientIsCreated(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.post_patients_id_anonymize(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        self.assertIn('ID', result.keys())
        self.assertIn('Path', result.keys())
        self.assertIn('PatientID', result.keys())
        self.assertIn(result['ID'], self.orthanc.get_patients())
        self.assertIn(
            'Anonymized',
            self.orthanc.get_patients_id(result['ID'])['MainDicomTags']['PatientName']
        )

    def test_givenOrthancWithoutAPatient_whenAnonymizeAPatient_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.post_patients_id_anonymize(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAPatient_whenArchivingAPatient_thenResultIsBytesOfAValidZipFile(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.post_patients_id_archive(a_patient.IDENTIFIER)

        self.assertIsInstance(result, bytes)
        with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
            file_handler.write(result)

        a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
        self.assertIsNone(a_zip_file.testzip())
        os.remove(a_patient.ZIP_FILE_PATH)

    def test_givenOrthancWithoutAPatient_whenArchivingAPatient_thenRaiseHTTPError(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.post_patients_id_archive(a_patient.IDENTIFIER)
        )
