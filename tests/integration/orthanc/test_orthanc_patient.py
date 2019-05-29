# coding: utf-8
# author: gabriel couture
import unittest

from tests.integration import setup_server


class TestOrthancPatient(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global orthanc_subprocess
        orthanc_subprocess = setup_server.setup_orthanc_server()

        setup_server.setup_data()

    @classmethod
    def tearDownClass(cls) -> None:
        setup_server.clear_data()

        global orthanc_subprocess
        setup_server.stop_orthanc_server_and_remove_data_directory(orthanc_subprocess)
        del orthanc_subprocess

    def test_something(self):
        self.assertEqual(True, True)
