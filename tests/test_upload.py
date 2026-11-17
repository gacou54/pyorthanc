import os
import shutil
import tempfile
import zipfile
from unittest.mock import patch

import httpx2
import pydicom
import pytest
from pydicom.data import get_testdata_file

from pyorthanc import upload


def test_upload_with_path(client):
    assert len(client.get_patients()) == 0
    path = get_testdata_file('CT_small.dcm')

    instances = upload(client, path)

    assert len(instances) == 1
    assert len(client.get_patients()) == 1


def test_upload_with_ds(client):
    assert len(client.get_patients()) == 0
    ds = pydicom.dcmread(get_testdata_file('CT_small.dcm'))

    instances = upload(client, ds)

    assert len(instances) == 1
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

        instances = upload(client, zip_filepath)

    assert len(instances) == 2
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

        instances = upload(client, tmpdirname)
        # Only one patient since only rtplan.dcm is in a direct directory
        assert len(instances) == 1
        assert len(client.get_patients()) == 1

        # Upload everything
        instances = upload(client, tmpdirname, recursive=True)
        assert len(instances) == 3
        assert len(client.get_patients()) == 3


def test_upload_with_bad_path(client):
    with pytest.raises(FileNotFoundError):
        upload(client, 'bad_path')


def test_upload_with_zip_without_dicom(client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        non_dicom_file_path = __file__

        zip_filepath = os.path.join(tmpdirname, 'non_dicom_files.zip')
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(non_dicom_file_path, os.path.basename(non_dicom_file_path))

        instances = upload(client, zip_filepath)

        assert len(instances) == 0
        assert len(client.get_patients()) == 0


def test_upload_with_directory_without_dicom(client):
    instances = upload(client, 'pyorthanc')

    assert len(instances) == 0
    assert len(client.get_patients()) == 0


def test_upload_while_checking_if_instance_exists(client):
    path = get_testdata_file('CT_small.dcm')

    with patch('pyorthanc.client.Orthanc.get_instances_id_metadata') as mock_get_instance:
        with patch('pyorthanc.client.Orthanc.post_instances', return_value={'ID': 'test-instance-id'}) as mock_post_instances:
            mock_get_instance.side_effect = httpx2.HTTPError('Instance already exists')
            instances = upload(client, path, check_before_upload=True)
            assert len(instances) == 1

            mock_get_instance.side_effect = None
            instances = upload(client, path, check_before_upload=True)
            assert len(instances) == 1

            assert mock_post_instances.call_count == 1  # Should only be called once
            assert mock_get_instance.call_count == 2  # Call 2 times to check if an instance exists before upload


def test_upload_zip_while_checking_with_force(client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_filepath = os.path.join(tmpdirname, 'dicom_files.zip')
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(get_testdata_file('CT_small.dcm'), 'CT_small.dcm')

        instances = upload(client, zip_filepath, check_before_upload=True, force=True)

    assert [i.id_ for i in instances] == ['f689ddd2-662f8fe1-8b18180d-ec2a2cee-937917af']


def test_upload_file_without_preamble_while_checking_with_force(client, tmp_dir):
    path = os.path.join(tmp_dir, 'without_preamble.dcm')
    with open(get_testdata_file('CT_small.dcm'), 'rb') as f, open(path, 'wb') as f2:
        f2.write(f.read()[132:])  # Removing the 128-byte preamble and the "DICM" prefix

    first = upload(client, path, check_before_upload=True, force=True)

    with patch('pyorthanc.client.Orthanc.post_instances') as mock_post_instances:
        second = upload(client, path, check_before_upload=True, force=True)

    assert [i.id_ for i in first] == [i.id_ for i in second] == ['f689ddd2-662f8fe1-8b18180d-ec2a2cee-937917af']
    mock_post_instances.assert_not_called()


def test_upload_file_without_preamble_while_checking_without_force(client, tmp_dir):
    path = os.path.join(tmp_dir, 'without_preamble.dcm')
    with open(get_testdata_file('CT_small.dcm'), 'rb') as f, open(path, 'wb') as f2:
        f2.write(f.read()[132:])  # Removing the 128-byte preamble and the "DICM" prefix

    upload(client, path)

    # Without force, the file cannot be read by pydicom, so it is uploaded again
    with patch('pyorthanc.client.Orthanc.post_instances', return_value={'ID': 'an-id'}) as mock_post_instances:
        upload(client, path, check_before_upload=True)

    mock_post_instances.assert_called_once()
