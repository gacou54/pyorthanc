# coding: utf-8
# author: gabriel couture
from typing import List, Dict

from pyorthanc.datastructure.tree.instance import Instance
from pyorthanc.orthanc import Orthanc


class Series:
    """Represent an series that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    def __init__(self, series_identifier: str, orthanc: Orthanc) -> None:
        """Constructor

        Parameters
        ----------
        series_identifier : Orthanc series identifier
        orthanc : Orthanc object
        """
        self.orthanc: Orthanc = orthanc

        self.series_identifier: str = series_identifier

        self.instances: List[Instance] = []

    def get_instances(self) -> List[Instance]:
        """Get series instance

        Returns
        -------
        List[Instance]
            List of the series's Instance.
        """
        return list(self.instances)

    def get_identifier(self) -> str:
        """Get series identifier

        Returns
        -------
        str
            Series identifier.
        """
        return self.series_identifier

    def get_main_information(self) -> Dict:
        """Get series main information

        Returns
        -------
        Dict
            Dictionary of series main information.
        """
        return self.orthanc.get_series_information(self.series_identifier).json()

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

    def _build_instances(self) -> List[Instance]:
        """Build a list of the series's instances

        Returns
        -------
        List[Instance]
            List of the series instances.
        """
        instance_identifiers = self.orthanc.get_series_instance_information(
            self.series_identifier).json()

        self.instances =  list(map(
            lambda i: Instance(i['ID'], self.orthanc),
            instance_identifiers
        ))

    def __str__(self):
        return f'Series (identifier={self.get_identifier()})'
