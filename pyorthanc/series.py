# coding: utf-8
# author: gabriel couture
from typing import List, Dict

from pyorthanc.instance import Instance
from pyorthanc.orthanc import Orthanc


class Series:
    """Represent an series that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    def __init__(
            self, series_identifier: str,
            orthanc: Orthanc,
            series_information: Dict = None) -> None:
        """Constructor

        Parameters
        ----------
        series_identifier
            Orthanc series identifier.
        orthanc
            Orthanc object.
        series_information
            Dictionary of series information.
        """
        self.orthanc = orthanc

        self.identifier = series_identifier
        self.information = series_information

        self.instances: List[Instance] = []

    def get_instances(self) -> List[Instance]:
        """Get series instance

        Returns
        -------
        List[Instance]
            List of the series's Instance.
        """
        return self.instances

    def get_identifier(self) -> str:
        """Get series identifier

        Returns
        -------
        str
            Series identifier.
        """
        return self.identifier

    def get_uid(self) -> str:
        """Get SeriesInstanceUID

        Returns
        -------
        str
            SeriesInstanceUID
        """
        return self.get_main_information()['MainDicomTags']['SeriesInstanceUID']

    def get_main_information(self) -> Dict:
        """Get series main information

        Returns
        -------
        Dict
            Dictionary of series main information.
        """
        if self.information is None:
            self.information = self.orthanc.get_series_information(
                self.identifier)

        return self.information

    def get_manufacturer(self) -> str:
        """Get the manufacturer

        Returns
        -------
        str
            The manufacturer.
        """
        return self.get_main_information()['MainDicomTags']['Manufacturer']

    def get_parent_study_identifier(self) -> str:
        """Get the parent study identifier

        Returns
        -------
        str
            The parent study identifier.
        """
        return self.get_main_information()['ParentStudy']

    def get_modality(self) -> str:
        """Get series modality

        Returns
        -------
        str
            Series modality.
        """
        return self.get_main_information()['MainDicomTags']['Modality']

    def get_series_number(self) -> str:
        """Get series number

        Returns
        -------
        str
            Series number.
        """
        return self.get_main_information()['MainDicomTags']['SeriesNumber']

    def build_instances(self) -> None:
        """Build a list of the series's instances
        """
        instance_identifiers = self.orthanc.get_series_instance_information(
            self.identifier
        )

        self.instances = list(map(
            lambda i: Instance(i['ID'], self.orthanc),
            instance_identifiers
        ))

    def __str__(self):
        return f'Series (identifier={self.get_identifier()})'

    def is_empty(self) -> bool:
        """Check if series is empty

        Returns
        -------
        bool
            True if series has no instance
        """
        return self.instances == []
