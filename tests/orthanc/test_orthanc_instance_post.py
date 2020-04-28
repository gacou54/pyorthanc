# coding: utf-8
# author: gabriel couture
import unittest

import requests

from pyorthanc import Orthanc
from tests import setup_server


class TestOrthancInstancePosts(unittest.TestCase):

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

    def given_data_in_orthanc_server(self):
        setup_server.setup_data()

    def test_givenRawDicomData_whenPostingInstances_thenInstancesIsStored(self):
        with open('./tests/data/dicom_files/RTSTRUCT.dcm', 'rb') as fh:
            data = fh.read()

        self.orthanc.post_instances(data)

        self.assertEqual(len(self.orthanc.get_instances()), 1)

    def test_givenBadDicomData_whenPostingInstances_thenInstancesIsStored(self):
        with open('./tests/__init__.py', 'rb') as fh:
            data = fh.read()

        self.assertRaises(
            requests.HTTPError,
            lambda: self.orthanc.post_instances(data)
        )
