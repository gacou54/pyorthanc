from datetime import datetime

import pytest

from pyorthanc.jobs import Job, State


@pytest.fixture
def job(patient):
    job = patient.anonymize(asynchronous=True)

    return job


def test_job_attributes(job: Job):
    job.block_until_completion()

    assert job.state == State.success

    assert isinstance(job.content, dict)
    assert job.type == 'ResourceModification'
    assert job.progress == 100
    assert job.priority == 0

    assert isinstance(job.effective_runtime, float)
    assert isinstance(job.creation_time, datetime)
    assert isinstance(job.timestamp, datetime)
    assert (job.completion_time is None) or isinstance(job.completion_time, datetime)

    assert job.error.code == 0
    assert job.error.description == 'Success'
