# coding: utf-8
# author: gabriel couture
from datetime import datetime
from typing import List, Dict

from pyorthanc.series import Series
from pyorthanc.orthanc import Orthanc


class Study:
    """Represent an study that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    def __init__(
            self, study_identifier: str,
            orthanc: Orthanc,
            study_information: Dict = None) -> None:
        """Constructor

        Parameters
        ----------
        study_identifier
            Orthanc study identifier.
        orthanc
            Orthanc object.
        study_information
            Dictionary of study's information.
        """
        self.orthanc = orthanc

        self.identifier = study_identifier
        self.information = study_information

        self.series: List[Series] = []

    def get_identifier(self) -> str:
        """Get Study identifier

        Returns
        -------
        str
            Study identifier
        """
        return self.identifier

    def get_main_information(self) -> Dict:
        """Get Study information

        Returns
        -------
        Dict
            Dictionary of study information
        """
        if self.information is None:
            self.information = self.orthanc.get_study_information(
                self.identifier
            )

        return self.information

    def get_referring_physician_name(self) -> str:
        """Get referring physician name

        Returns
        -------
        str
            Referring physician Name.
        """
        return self.get_main_information()['MainDicomTags']['ReferringPhysicianName']

    def get_date(self) -> datetime:
        """Get study date

        The date have precision to the second (if available).

        Returns
        -------
        datetime
            Study date
        """
        date_string = self.get_main_information()['MainDicomTags']['StudyDate']
        time_string = self.get_main_information()['MainDicomTags']['StudyTime']

        try:
            return datetime(
                year=int(date_string[:4]),
                month=int(date_string[4:6]),
                day=int(date_string[6:8]),
                hour=int(time_string[:2]),
                minute=int(time_string[2:4]),
                second=int(time_string[4:6])
            )
        except ValueError:
            return datetime(
                year=int(date_string[:4]),
                month=int(date_string[4:6]),
                day=int(date_string[6:8]),
            )

    def get_id(self) -> str:
        """Get Study ID

        Returns
        -------
        str
            Study ID
        """
        try:
            return self.get_main_information()['MainDicomTags']['StudyID']
        except KeyError:
            return ''

    def get_uid(self) -> str:
        """Get StudyInstanceUID

        Returns
        -------
        str
            StudyInstanceUID
        """
        return self.get_main_information()['MainDicomTags']['StudyInstanceUID']

    def get_parent_patient_identifier(self) -> str:
        """Get the Orthanc identifier of the parent patient

        Returns
        -------
        str
            Parent patient's identifier.
        """
        return self.get_main_information()['ParentPatient']

    def get_patient_information(self) -> Dict:
        """Get patient information

        Returns
        -------
        Dict
            Patient general information.
        """
        return self.get_main_information()['PatientMainDicomTags']

    def get_series(self) -> List[Series]:
        """Get Study series

        Returns
        -------
        List[Series]
            List of study's Series
        """
        return self.series

    def build_series(self) -> None:
        """Build a list of the study's series
        """
        series_identifiers = self.orthanc.get_study_series_information(
            self.identifier
        )

        self.series = list(map(
            lambda i: Series(i['ID'], self.orthanc),
            series_identifiers
        ))

    def __str__(self):
        return f'Study (id={self.get_id()}, identifier={self.get_identifier()})'

    def trim(self) -> None:
        """Delete empty series
        """
        self.series = list(filter(
            lambda series: not series.is_empty(),
            self.series
        ))

    def is_empty(self) -> bool:
        """Check if series is empty

        Returns
        -------
        bool
            True if study has no instance
        """
        return self.series == []
