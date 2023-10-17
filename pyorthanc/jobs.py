import time
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from . import util
from ._orthanc_sdk_enums import ErrorCode
from .client import Orthanc


class State(Enum):
    """Job state enum"""
    failure = 'Failure'
    paused = 'Paused'
    pending = 'Pending'
    retry = 'Retry'
    running = 'Running'
    success = 'Success'


class Job:
    """Job class to follow a Job in Orthanc"""

    def __init__(self, id_: str, client: Orthanc):
        client = util.ensure_non_raw_response(client)

        self.id_ = id_
        self.client = client

    @property
    def state(self) -> State:
        state = self.get_information()['State']

        return State(state)

    @property
    def content(self) -> Dict:
        return self.get_information()['Content']

    @property
    def type(self) -> str:
        return self.get_information()['Type']

    @property
    def creation_time(self) -> datetime:
        creation_time = self.get_information()['CreationTime'].split('T')
        date = creation_time[0]
        time = creation_time[1]

        return util.make_datetime_from_dicom_date(date, time)

    @property
    def effective_runtime(self) -> float:
        runtime = self.get_information()['EffectiveRuntime']

        return float(runtime)

    @property
    def priority(self) -> int:
        return int(self.get_information()['Priority'])

    @property
    def progress(self) -> int:
        return int(self.get_information()['Progress'])

    @property
    def error(self) -> ErrorCode:
        info = self.get_information()

        return ErrorCode(info['ErrorCode'])

    @property
    def error_details(self) -> Optional[str]:
        info = self.get_information()

        if 'ErrorDetails' in info:
            return info['ErrorDetails']

        return None

    @property
    def timestamp(self) -> datetime:
        timestamp = self.get_information()['Timestamp'].split('T')
        date = timestamp[0]
        time = timestamp[1]

        return util.make_datetime_from_dicom_date(date, time)

    @property
    def completion_time(self) -> Optional[datetime]:
        info = self.get_information()

        if 'CompletionTime' not in info:
            return

        completion_time = self.get_information()['CompletionTime'].split('T')
        date = completion_time[0]
        time = completion_time[1]

        return util.make_datetime_from_dicom_date(date, time)

    def wait_until_completion(self, time_interval: int = 2) -> None:
        """Stop execution until job is not Pending/Running

        Parameters
        ----------
        time_interval
            Time interval to check the job status, default 2s.
        """
        while self.state in [State.pending, State.running]:
            time.sleep(time_interval)

    def get_information(self):
        return self.client.get_jobs_id(self.id_)
