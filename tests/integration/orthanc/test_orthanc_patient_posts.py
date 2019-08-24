# coding: utf-8
# author: gabriel couture
import unittest

import requests

from pyorthanc import Orthanc
from tests.integration import setup_server
from tests.integration.data import a_patient


class TestOrthancPatientPosts(unittest.TestCase):

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

    def test_givenOrthancWithAPatient_whenAnonymizeAPatient_thenResultIsIdentifiersOfNewAnonymousPatientAndANewAnonymousPatientIsCreated(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.anonymize_patient(a_patient.IDENTIFIER)

        self.assertIsInstance(result, dict)
        self.assertIn('ID', result.keys())
        self.assertIn('Path', result.keys())
        self.assertIn('PatientID', result.keys())
        self.assertIn(result['ID'], self.orthanc.get_patients())
        self.assertEqual(
            'Anonymized1',
            self.orthanc.get_patient_information(result['ID'])['MainDicomTags']['PatientName']
        )
