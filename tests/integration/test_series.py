# coding: utf-8
# author: Gabriel Couture
import unittest

from pyorthanc import Orthanc
from pyorthanc.datastructure import Series
from tests.integration import setup_server
from tests.integration.data import a_series


class TestSeries(unittest.TestCase):

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

        self.series = Series(
            a_series.IDENTIFIER,
            Orthanc(setup_server.ORTHANC_URL)
        )

    def tearDown(self) -> None:
        self.series = None
        setup_server.clear_data()

    def test_givenASeries_whenGettingMainInformation_thenResultIsExpectedSeriesInformation(self):
        keys_to_exclude = {'LastUpdate'}

        result = self.series.get_main_information()

        self.assertDictEqual(
            {key: value for key, value in result.items() if key not in keys_to_exclude},
            {key: value for key, value in a_series.INFORMATION.items() if key not in keys_to_exclude},
        )

    def test_givenASeries_whenGettingManufacturer_thenResultIsExpectedManufacturer(self):
        result = self.series.get_manufacturer()

        self.assertEqual(result, a_series.MANUFACTURER)

    def test_givenASeries_whenGettingParentStudyIdentifier_thenResultIsExpectedParentStudyIdentifier(self):
        result = self.series.get_parent_study_identifier()

        self.assertEqual(result, a_series.PARENT_STUDY)

    def test_givenASeries_whenBuildingInstances_thenPatientHasInstances(self):
        self.series.build_instances()

        self.assertEqual(
            len(self.series.get_instances()),
            len(a_series.INSTANCES)
        )
