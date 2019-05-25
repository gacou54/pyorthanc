# coding: utf-8
# author: gabriel couture
from typing import List, Dict

from pyorthanc.datastructure.tree.series import Series
from pyorthanc.orthanc import Orthanc


class Study:
    """Represent an series that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    def __init__(self, study_identifier: str, orthanc: Orthanc) -> None:
        """Constructor

        Parameters
        ----------
        study_identifier
            Orthanc study identifier.
        orthanc
            Orthanc object.
        """
        self.orthanc: Orthanc = orthanc

        self.study_identifier: str = study_identifier

        self.series: List[Series] = []

    def get_identifier(self) -> str:
        """Get Study identifier

        Returns
        -------
        str
            Study identifier
        """
        return self.study_identifier

    def get_main_information(self) -> Dict:
        """Get Study information

        Returns
        -------
        Dict
            Dictionary of study information
        """
        return self.orthanc.get_study_information(self.study_identifier).json()

    def get_date(self) -> str:
        """Get study date

        Returns
        -------
        str
            Study date
        """
        return self.get_main_information()['MainDicomTags']['StudyDate']

    def get_time(self) -> str:
        """Get Study time

        Returns
        -------
        str
            Study time
        """
        return self.get_main_information()['MainDicomTags']['StudyTime']

    def get_id(self) -> str:
        """Get Study ID

        Returns
        -------
        str
            Study ID
        """
        return self.get_main_information()['MainDicomTags']['StudyID']

    def get_description(self) -> str:
        """Get study description

        Returns
        -------
        str
            Study description
        """
        return self.get_main_information()['MainDicomTags']['StudyDescription']

    def get_series(self) -> List[Series]:
        """Get Study series

        Returns
        -------
        List[Series]
            List of study's Series
        """
        return list(self.series)

    def build_series(self) -> None:
        """Build a list of the study's series

        Returns
        -------
        None
        """
        series_identifiers = self.orthanc.get_study_series_information(
            self.study_identifier).json()

        self.series = list(map(
            lambda i: Series(i['ID'], self.orthanc),
            series_identifiers
        ))

    def __str__(self):
        return f'Study (id={self.get_id()}, identifier={self.get_identifier()})'
