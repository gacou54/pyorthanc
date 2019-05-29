# coding: utf-8
# author: gabriel couture
import unittest
from typing import List

from pyorthanc import Orthanc
from tests.integration import setup_server


class TestOrthancPatient(unittest.TestCase):

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

    def test_givenPatientInOrthanc_whenGettingPatients_thenResultIdAListOfPatientIdentifierStrings(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.get_patients().json()

        self.assertIsInstance(result, list)
        for patient_identifier in result:
            self.assertIsInstance(patient_identifier, str)
