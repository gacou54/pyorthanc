# coding: utf-8
# author: Gabriel Couture
import unittest

from pyorthanc import Orthanc
from pyorthanc.datastructure import Patient
from tests.integration import setup_server
from tests.integration.data import a_patient


class TestPatient(unittest.TestCase):

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
        setup_server.setup_data()
        self.patient = Patient(
            a_patient.IDENTIFIER,
            Orthanc(setup_server.ORTHANC_URL)
        )

    def tearDown(self) -> None:
        self.patient = None
        setup_server.clear_data()

    def test_givenAPatient_whenGettingMainInformation_thenResultIsExpectedPatientInformation(self):
        keys_to_exclude = {'LastUpdate'}

        result = self.patient.get_main_information()

        self.assertEqual(
            {key: value for key, value in result.items() if key not in keys_to_exclude},
            {key: value for key, value in a_patient.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenAPatient_whenGettingPatientID_thenResultIsExpectedPatientID(self):
        result = self.patient.get_id()

        self.assertEqual(result, a_patient.ID)

    def test_givenAPatient_whenGettingPatientName_thenResultIsExpectedPatientName(self):
        result = self.patient.get_patient_name()

        self.assertEqual(result, a_patient.NAME)

    def test_givenAPatient_whenGettingPatientSex_thenResultIsExpectedSex(self):
        result = self.patient.get_patient_sex()

        self.assertEqual(result, a_patient.SEX)

    def test_givenAPatient_whenBuildingStudies_thenPatientHasStudies(self):
        self.patient.build_studies()

        self.assertEqual(
            len(self.patient.get_studies()),
            len(a_patient.STUDIES)
        )

    def test_givenAPatientWithEmptyStudies_whenTrimPatient_thenEmptyStudiesGetsDeleted(self):
        self.patient.build_studies()  # When getting building, studies do not get built by default
        expected_number_of_study = 0

        self.patient.trim()

        self.assertEqual(
            expected_number_of_study,
            len(self.patient.get_studies())
        )
