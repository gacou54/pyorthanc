import glob
import shutil

import pytest

from pyorthanc.retrieve import retrieve_and_write_patients

PATH = 'tmp'


@pytest.fixture
def path():
    yield PATH

    shutil.rmtree(PATH)


def test_retrieve_and_write_patients(patient, study, series, instance, path):
    retrieve_and_write_patients([patient], path)

    assert f'{path}/{patient.patient_id}/{study.uid}/{series.modality}-1/{instance.uid}.dcm' in glob.glob(
        f'{path}/**/*.dcm',
        recursive=True
    )
