import unittest

import httpx

from pyorthanc import Orthanc
from tests.setup_server import ORTHANC_1, clear_data, add_data


class TestOrthancInstancePosts(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)

    def given_data_in_orthanc_server(self):
        add_data(ORTHANC_1)

    def test_givenRawDicomData_whenPostingInstances_thenInstancesIsStored(self):
        with open('tests/data/orthanc_1_test_data/RTSTRUCT.dcm', 'rb') as fh:
            data = fh.read()

        self.orthanc.post_instances(data)

        self.assertEqual(len(self.orthanc.get_instances()), 1)

    def test_givenBadDicomData_whenPostingInstances_thenInstancesIsStored(self):
        with open('./tests/__init__.py', 'rb') as fh:
            data = fh.read()

        self.assertRaises(
            httpx.HTTPError,
            lambda: self.orthanc.post_instances(data)
        )
