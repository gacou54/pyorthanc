# coding: utf-8
# author: gabriel couture
import unittest

from pyorthanc import Orthanc
from tests.integration import setup_server


class TestOrthancPatientGetter(unittest.TestCase):
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

    def test_givenOrthancWithData_whenDeletingPatientData_thenResultIsTrue(self):
        self.given_patient_in_orthanc_server()

        result = self.orthanc.delete_patient(TestOrthancPatientGetter.A_PATIENT_IDENTIFIER)

        self.assertTrue(result)

    def test_givenOrthancWithoutData_whenDeletingPatientData_thenResultIsFalse(self):
        result = self.orthanc.delete_patient(TestOrthancPatientGetter.A_PATIENT_IDENTIFIER)

        self.assertFalse(result)
