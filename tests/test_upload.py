import pydicom
from pydicom.data import get_testdata_file

from pyorthanc import upload


def test_upload_with_path(client):
    assert len(client.get_patients()) == 0
    path = get_testdata_file('CT_small.dcm')

    upload(client, path)

    assert len(client.get_patients()) == 1


def test_upload_with_ds(client):
    assert len(client.get_patients()) == 0
    ds = pydicom.dcmread(get_testdata_file('CT_small.dcm'))

    upload(client, ds)

    assert len(client.get_patients()) == 1


