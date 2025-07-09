import os
import shutil
import tempfile
import zipfile

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


def test_upload_with_zip(client):
    assert len(client.get_patients()) == 0
    with tempfile.TemporaryDirectory() as tmpdirname:
        ct_file_path = get_testdata_file('CT_small.dcm')
        mr_file_path = get_testdata_file('MR_small.dcm')

        zip_filepath = os.path.join(tmpdirname, 'dicom_files.zip')
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(ct_file_path, os.path.basename(ct_file_path))
            zipf.write(mr_file_path, os.path.basename(mr_file_path))

        upload(client, zip_filepath)

    assert len(client.get_patients()) == 2


def test_upload_with_directory(client):
    assert len(client.get_patients()) == 0
    with tempfile.TemporaryDirectory() as tmpdirname:
        rtplan_file_path = get_testdata_file('rtplan.dcm')
        mr_file_path = get_testdata_file('MR_small.dcm')
        ct_file_path = get_testdata_file('CT_small.dcm')

        os.makedirs(os.path.join(tmpdirname, 'mr'))
        os.makedirs(os.path.join(tmpdirname, 'ct', 'other-dir'))  # This one is more deep

        shutil.copy(rtplan_file_path, os.path.join(tmpdirname, 'rtplan.dcm'))
        shutil.copy(mr_file_path, os.path.join(tmpdirname, 'mr', 'MR_small.dcm'))
        shutil.copy(ct_file_path, os.path.join(tmpdirname, 'ct', 'other-dir', 'CT_small.dcm'))

        upload(client, tmpdirname)
        # Only one patient since only rtplan.dcm is in a direct directory
        assert len(client.get_patients()) == 1

        # Upload everything
        upload(client, tmpdirname, recursive=True)
        assert len(client.get_patients()) == 3
