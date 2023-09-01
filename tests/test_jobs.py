from datetime import datetime

import pytest

from pyorthanc.jobs import ErrorCode, Job, State


@pytest.fixture
def job(patient):
    job = patient.anonymize_as_job()

    return job


def test_job_attributes(job: Job):
    job.wait_until_completion()

    assert job.state == State.success

    assert isinstance(job.content, dict)
    assert job.type == 'ResourceModification'
    assert job.progress == 100
    assert job.priority == 0

    assert isinstance(job.effective_runtime, float)
    assert isinstance(job.creation_time, datetime)
    assert isinstance(job.timestamp, datetime)
    assert (job.completion_time is None) or isinstance(job.completion_time, datetime)

    assert job.error == ErrorCode.SUCCESS
    assert job.error_details == ''
