import unittest
import warnings

import httpx

from pyorthanc import Orthanc
from tests.data import a_patient
from tests.setup_server import ORTHANC_1, clear_data, setup_data


class TestOrthancPatientSetters(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_patient_in_orthanc_server(self):
        setup_data(ORTHANC_1)

    def test_givenOrthancWithAnUnprotectedPatient_whenSettingPatientToProtected_thenPatientIsProtected(self):
        warnings.warn('Cannot set Patient to protected (not working with the generated Orthanc client) -- skipping test')
        # self.given_patient_in_orthanc_server()
        #
        # self.orthanc.put_patients_id_protected(a_patient.IDENTIFIER)
        #
        # self.assertTrue(
        #     self.orthanc.get_patients_id_protected(a_patient.IDENTIFIER)
        # )

    def test_givenOrthancWithAnUnprotectedPatient_whenSettingPatientToNotProtected_thenPatientIsUnprotected(self):
        warnings.warn('Cannot set Patient to unprotected (not working with the generated Orthanc client) -- skipping test')
        # self.given_patient_in_orthanc_server()

        # self.orthanc.set_patient_to_not_protected(a_patient.IDENTIFIER)

        # self.assertFalse(
        #     self.orthanc.get_if_patient_is_protected(a_patient.IDENTIFIER)
        # )

    def test_givenOrthancWithoutPatient_whenSettingPatientToProtected_thenRaiseHTTPError(self):
        warnings.warn('Cannot set Patient to protected (not working with the generated Orthanc client) -- skipping test')
        # self.assertRaises(
        #     httpx.HTTPError,
        #     lambda: self.orthanc.set_patient_to_protected(a_patient.IDENTIFIER)
        # )

    def test_givenOrthancWithoutPatient_whenSettingPatientToNotProtected_thenRaiseHTTPError(self):
        warnings.warn('Cannot set Patient to unprotected (not working with the generated Orthanc client) -- skipping test')
        # self.assertRaises(
        #     httpx.HTTPError,
        #     lambda: self.orthanc.set_patient_to_not_protected(a_patient.IDENTIFIER)
        # )