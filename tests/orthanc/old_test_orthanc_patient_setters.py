# coding: utf-8
# author: gabriel couture
import unittest

from requests import HTTPError

from pyorthanc import Orthanc
from tests import setup_server
from tests.data import a_patient


class TestOrthancPatientSetters(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global orthanc_subprocess
        orthanc_subprocess = setup_server.setup_orthanc_server()

    @classmethod
    def tearDownClass(cls) -> None:
        global orthanc_subprocess
        setup_server.stop_server_and_remove_data(orthanc_subprocess)
        del orthanc_subprocess

    def setUp(self) -> None:
        self.orthanc = Orthanc(setup_server.ORTHANC_1)

    def tearDown(self) -> None:
        self.orthanc = None
        setup_server.clear_data()

    def given_patient_in_orthanc_server(self):
        setup_server.setup_data()

    def test_givenOrthancWithAnUnprotectedPatient_whenSettingPatientToProtected_thenPatientIsProtected(self):
        self.given_patient_in_orthanc_server()

        self.orthanc.set_patient_to_protected(a_patient.IDENTIFIER)

        self.assertTrue(
            self.orthanc.get_if_patient_is_protected(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithAnUnprotectedPatient_whenSettingPatientToNotProtected_thenPatientIsUnprotected(self):
        self.given_patient_in_orthanc_server()

        self.orthanc.set_patient_to_not_protected(a_patient.IDENTIFIER)

        self.assertFalse(
            self.orthanc.get_if_patient_is_protected(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithoutPatient_whenSettingPatientToProtected_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.set_patient_to_protected(a_patient.IDENTIFIER)
        )

    def test_givenOrthancWithoutPatient_whenSettingPatientToNotProtected_thenRaiseHTTPError(self):
        self.assertRaises(
            HTTPError,
            lambda: self.orthanc.set_patient_to_not_protected(a_patient.IDENTIFIER)
        )
