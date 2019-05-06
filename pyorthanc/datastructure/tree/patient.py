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

    def __init__(self, patient_identifier: str, orthanc: Orthanc) -> None:
        """Constructor

        Parameters
        ----------
        patient_identifier : Orthanc patient identifier
        orthanc : Orthanc object
        """
        self.orthanc: Orthanc = orthanc

        self.patient_identifier: str = patient_identifier

        self.studies: List[Study] = self._build_studies()

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
        return self.orthanc.get_patient_information(
            self.patient_identifier).json()

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

    def _build_studies(self) -> List[Study]:
        """Build a list of the patient's studies

        Returns
        -------
        List[Study]
            List of the patient's studies
        """
        study_identifiers = self.orthanc.get_patient_studies(
            self.patient_identifier).json()
        print(study_identifiers)

        return list(map(lambda i: Study(i['ID'], self.orthanc), study_identifiers))

    def __str__(self):
        return f'Patient (id={self.get_id()}, identifier={self.get_identifier()})'
