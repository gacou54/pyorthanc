# coding: utf-8
# author: Gabriel Couture
import unittest

from pyorthanc import Orthanc
from pyorthanc.datastructure import Study
from tests.integration import setup_server
from tests.integration.data import a_study


class TestStudy(unittest.TestCase):

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

        self.study = Study(
            a_study.IDENTIFIER,
            Orthanc(setup_server.ORTHANC_URL)
        )

    def tearDown(self) -> None:
        self.study = None
        setup_server.clear_data()

    def test_givenAStudy_whenGettingMainInformation_thenResultIsExpectedStudyInformation(self):
        keys_to_exclude = {'LastUpdate'}

        result = self.study.get_main_information()

        self.assertDictEqual(
            {key: value.sort() if type(value) == list else value for key, value in result.items() if key not in keys_to_exclude},
            {key: value.sort() if type(value) == list else value for key, value in a_study.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenAStudy_whenGettingParentPatientIdentifier_thenResultIsExpectedParentPatientIdentifier(self):
        result = self.study.get_parent_patient_identifier()

        self.assertEqual(result, a_study.PARENT_PATIENT_IDENTIFIER)

    def test_givenAStudy_whenGettingPatientMainInformation_thenResultIsExpectedPatientMainInformation(self):
        result = self.study.get_patient_information()

        self.assertDictEqual(result, a_study.PATIENT_MAIN_INFORMATION)

    def test_givenAStudy_whenGettingStudyTime_thenResultIsExpectedTime(self):
        result = self.study.get_time()

        self.assertEqual(result, a_study.TIME)

    def test_givenAStudy_whenGettingStudyDate_thenResultIsExpectedDate(self):
        result = self.study.get_date()

        self.assertEqual(result, a_study.DATE)

    def test_givenAStudy_whenGettingStudyID_thenResultIsExpectedID(self):
        result = self.study.get_id()

        self.assertEqual(result, a_study.ID)

    def test_givenAStudy_whenGettingReferringPhysicianName_thenResultIsExpectedReferringPhysicianName(self):
        result = self.study.get_referring_physician_name()

        self.assertEqual(result, a_study.REFERRING_PHYSICIAN_NAME)

    def test_givenAStudy_whenBuildingSeries_thenStudyHasSeries(self):
        self.study.build_series()

        self.assertEqual(
            len(self.study.get_series()),
            len(a_study.SERIES)
        )

    def test_givenAStudyWithEmptySeries_whenTrimStudy_thenEmptySeriesGetsDeleted(self):
        self.study.build_series()  # When getting building, series do not get built by default
        expected_number_of_series = 0

        self.study.trim()

        self.assertEqual(
            expected_number_of_series,
            len(self.study.get_series())
        )
