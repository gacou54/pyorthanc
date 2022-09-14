import unittest

import httpx

from pyorthanc import Orthanc
from tests.data import a_patient
from tests.setup_server import ORTHANC_1, clear_data, add_data


class TestOrthancPatientDeleters(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_patient_in_orthanc_server(self):
        add_data(ORTHANC_1)

    def test_givenOrthancWithPatient_whenDeletingPatientData_thenResultIsTrue(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.delete_patients_id(a_patient.IDENTIFIER)

        self.assertIsNone(result)

    def test_givenOrthancWithoutPatient_whenDeletingPatientData_thenResultIsFalse(self):
        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.delete_patients_id(a_patient.IDENTIFIER)
        )
