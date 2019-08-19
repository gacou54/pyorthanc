# coding: utf-8
# author: gabriel couture
from typing import List, Dict

from pyorthanc.datastructure.tree.study import Study
from pyorthanc.orthanc import Orthanc


class Patient:
    """Represent an Patient that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Patient
    """

    def __init__(
            self, patient_identifier: str,
            orthanc: Orthanc,
            patient_information: Dict = None) -> None:
        """Constructor

        Parameters
        ----------
        patient_identifier
            Orthanc patient identifier.
        orthanc
            Orthanc object.
        patient_information
            Dictionary of patient's information.
        """
        self.orthanc = orthanc

        self.patient_identifier = patient_identifier
        self.patient_information = patient_information

        self.studies: List[Study] = []

    def get_identifier(self) -> str:
        """Get patient identifier

        Returns
        -------
        str
            Patient identifier
        """
        return self.patient_identifier

    def get_main_information(self) -> Dict:
        """Get Patient information

        Returns
        -------
        Dict
            Dictionary of patient main information.
        """
        if self.patient_information is None:
            self.patient_information = self.orthanc.get_patient_information(
                self.patient_identifier)

        return self.patient_information

    def get_id(self) -> str:
        """Get patient ID

        Returns
        -------
        str
            Patient ID
        """
        return self.get_main_information()['MainDicomTags']['PatientID']

    def get_patient_name(self) -> str:
        """Get patient name

        Returns
        -------
        str
            Patient name
        """
        return self.get_main_information()['MainDicomTags']['PatientName']

    def get_patient_sex(self) -> str:
        """Get patient sex

        Returns
        -------
        str
            Patient sex
        """
        return self.get_main_information()['MainDicomTags']['PatientSex']

    def get_studies(self) -> List[Study]:
        """Get patient's studies

        Returns
        -------
        List[Study]
            List of the patient's studies
        """
        return list(self.studies)

    def build_studies(self) -> None:
        """Build a list of the patient's studies
        """
        study_identifiers = self.orthanc.get_patient_studies(
            self.patient_identifier
        )

        self.studies = list(map(
            lambda i: Study(i['ID'], self.orthanc),
            study_identifiers
        ))

    def __str__(self):
        return f'Patient (id={self.get_id()}, identifier={self.get_identifier()})'

    def trim(self) -> None:
        """Delete empty studies
        """
        for study in self.get_studies():
            study.trim()

        self.studies = list(filter(
            lambda study: not study.is_empty(), self.studies
        ))

    def is_empty(self) -> bool:
        """Check if studies is empty

        Returns
        -------
        bool
            True if patient has no instance
        """
        return self.studies == []
