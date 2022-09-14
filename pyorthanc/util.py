from datetime import datetime
from typing import Optional

from pyorthanc.async_client import AsyncOrthanc
from pyorthanc.client import Orthanc


def make_datetime_from_dicom_date(date: str, time: str = None) -> Optional[datetime]:
    """Attempt to decode date"""
    try:
        return datetime(
            year=int(date[:4]),
            month=int(date[4:6]),
            day=int(date[6:8]),
            hour=int(time[:2]),
            minute=int(time[2:4]),
            second=int(time[4:6])
        )
    except (ValueError, TypeError):
        try:
            return datetime(
                year=int(date[:4]),
                month=int(date[4:6]),
                day=int(date[6:8]),
            )
        except (ValueError, TypeError):
            return None


def async_to_sync(orthanc: AsyncOrthanc) -> Orthanc:
    sync_orthanc = Orthanc(url=orthanc.url)
    sync_orthanc._auth = orthanc.auth

    return sync_orthanc


def sync_to_async(orthanc: Orthanc) -> AsyncOrthanc:
    async_orthanc = AsyncOrthanc(url=orthanc.url)
    async_orthanc._auth = orthanc.auth

    return async_orthanc
