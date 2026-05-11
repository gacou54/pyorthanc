import os
import tempfile
import zipfile
from unittest.mock import AsyncMock, patch

import httpx
import pydicom
import pytest
from pydicom.data import get_testdata_file

from pyorthanc import Instance, async_upload


@pytest.mark.asyncio
async def test_async_upload_with_path(async_client):
    path = get_testdata_file('CT_small.dcm')

    result = await async_upload(async_client, path)

    assert isinstance(result, list)
    assert isinstance(result[0], Instance)
    assert result[0].id_ == 'f689ddd2-662f8fe1-8b18180d-ec2a2cee-937917af'


@pytest.mark.asyncio
async def test_async_upload_with_ds(async_client):
    ds = pydicom.dcmread(get_testdata_file('CT_small.dcm'))

    result = await async_upload(async_client, ds)

    assert isinstance(result, list)
    assert isinstance(result[0], Instance)
    assert result[0].id_ == 'f689ddd2-662f8fe1-8b18180d-ec2a2cee-937917af'


@pytest.mark.asyncio
async def test_async_upload_with_zip(async_client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        ct_file_path = get_testdata_file('CT_small.dcm')
        mr_file_path = get_testdata_file('MR_small.dcm')

        zip_filepath = os.path.join(tmpdirname, 'dicom_files.zip')
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(ct_file_path, os.path.basename(ct_file_path))
            zipf.write(mr_file_path, os.path.basename(mr_file_path))

        result = await async_upload(async_client, zip_filepath)

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(i, Instance) for i in result)


@pytest.mark.asyncio
async def test_async_upload_with_directory(async_client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        rtplan_file_path = get_testdata_file('rtplan.dcm')
        mr_file_path = get_testdata_file('MR_small.dcm')
        ct_file_path = get_testdata_file('CT_small.dcm')

        for file_path in [rtplan_file_path, mr_file_path, ct_file_path]:
            with open(file_path, 'rb') as f:
                with open(os.path.join(tmpdirname, os.path.basename(file_path)), 'wb') as f2:
                    f2.write(f.read())

        result = await async_upload(async_client, tmpdirname)

    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(i, Instance) for i in result)


@pytest.mark.asyncio
async def test_async_upload_with_bad_path(async_client):
    with pytest.raises(FileNotFoundError):
        await async_upload(async_client, 'bad/path')


@pytest.mark.asyncio
async def test_async_upload_with_zip_without_dicom(async_client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        non_dicom_file_path = __file__

        zip_filepath = os.path.join(tmpdirname, 'non_dicom_files.zip')
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(non_dicom_file_path, os.path.basename(non_dicom_file_path))

        result = await async_upload(async_client, zip_filepath)

    assert result == []


@pytest.mark.asyncio
async def test_async_upload_with_directory_without_dicom(async_client, tmp_dir):
    result = await async_upload(async_client, tmp_dir)

    assert result == []


@pytest.mark.asyncio
async def test_async_upload_while_checking_if_instance_exists(async_client):
    path = get_testdata_file('CT_small.dcm')

    with patch('pyorthanc.async_client.AsyncOrthanc.get_instances_id_metadata', new_callable=AsyncMock) as mock_get_instance:
        with patch('pyorthanc.async_client.AsyncOrthanc.post_instances', new_callable=AsyncMock) as mock_post_instances:
            mock_post_instances.return_value = {'ID': 'test-instance-id'}

            mock_get_instance.side_effect = httpx.HTTPError('Instance already exists')
            instances = await async_upload(async_client, path, check_before_upload=True)
            assert len(instances) == 1

            mock_get_instance.side_effect = None
            mock_get_instance.return_value = {}  # Success
            instances = await async_upload(async_client, path, check_before_upload=True)
            assert len(instances) == 1

            assert mock_post_instances.call_count == 1  # Should only be called once
            assert mock_get_instance.call_count == 2  # Call 2 times to check if an instance exists before upload
