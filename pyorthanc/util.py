from datetime import datetime


def make_datetime_from_dicom_date(date: str, time: str) -> datetime:
    return datetime(
        year=int(date[:4]),
        month=int(date[4:6]),
        day=int(date[6:8]),
        hour=int(time[:2]),
        minute=int(time[2:4]),
        second=int(time[4:6])
    )
