# coding: utf-8
# author: gabriel couture
from typing import List, Dict

from pyorthanc.study import Study
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

        self.identifier = patient_identifier
        self.information = patient_information

        self.studies: List[Study] = []

    def get_identifier(self) -> str:
        """Get patient identifier

        Returns
        -------
        str
            Patient identifier
        """
        return self.identifier

    def get_main_information(self) -> Dict:
        """Get Patient information

        Returns
        -------
        Dict
            Dictionary of patient main information.
        """
        if self.information is None:
            self.information = self.orthanc.get_patient_information(
                self.identifier
            )

        return self.information

    def get_id(self) -> str:
        """Get patient ID

        Returns
        -------
        str
            Patient ID
        """
        return self.get_main_information()['MainDicomTags']['PatientID']

    def get_name(self) -> str:
        """Get patient name

        Returns
        -------
        str
            Patient name
        """
        return self.get_main_information()['MainDicomTags']['PatientName']

    def get_sex(self) -> str:
        """Get patient sex

        Returns
        -------
        str
            Patient sex
        """
        return self.get_main_information()['MainDicomTags']['PatientSex']

    def get_zip(self) -> bytes:
        """Get the bytes of the zip file

        Get the .zip file.

        Returns
        -------
        bytes
            Bytes of Zip file of the patient.

        Examples
        --------
        >>> from pyorthanc import Orthanc, Patient
        >>> a_patient = Patient(
        ...     'A_PATIENT_IDENTIFIER',
        ...     Orthanc('http://localhost:8042')
        ... )
        >>> bytes_content = a_patient.get_zip()
        >>> with open('patient_zip_file_path.zip', 'wb') as file_handler:
        ...     file_handler.write(bytes_content)

        """
        return self.orthanc.get_patient_zip(self.identifier)

    def get_patient_module(self) -> Dict:
        """Get patient module in a simplified version

        The method returns the DICOM patient module
        (PatientName, PatientID, PatientBirthDate, ...)

        Returns
        -------
        Dict
            DICOM Patient module.
        """
        return self.orthanc.get_patient_module_in_simplified_version(
            self.identifier
        )

    def is_protected(self) -> bool:
        """Get if patient is protected against recycling

        Protection against recycling: False means unprotected, True protected.

        Returns
        -------
        bool
            False means unprotected, True means protected.
        """
        return self.orthanc.get_if_patient_is_protected(
            self.identifier
        )

    def set_to_protected(self):
        """Set patient to protected state

        Returns
        -------
        None
            Nothing.
        """
        self.orthanc.set_patient_to_protected(self.identifier)

    def set_to_unprotected(self):
        """Set patient to unprotected state

        Returns
        -------
        None
            Nothing.
        """
        self.orthanc.set_patient_to_not_protected(self.identifier)

    def get_studies(self) -> List[Study]:
        """Get patient's studies

        Returns
        -------
        List[Study]
            List of the patient's studies
        """
        return self.studies

    def build_studies(self) -> None:
        """Build a list of the patient's studies
        """
        studies_information = self.orthanc.get_patient_studies_information(
            self.identifier
        )

        self.studies = list(map(
            lambda i: Study(i['ID'], self.orthanc),
            studies_information
        ))

    def anonymize(self) -> 'Patient':
        """Anonymize patient

        If no error is been raise, then it creates a new anonymous patient.
        Documentation: http://book.pyorthanc-server.com/users/anonymization.html

        Returns
        -------
        Patient
            A New anonymous patient.
        """
        new_anonymous_patient = self.orthanc.anonymize_patient(self.identifier)

        return Patient(new_anonymous_patient['ID'], self.orthanc)

    def __str__(self):
        return f'Patient (id={self.get_id()}, identifier={self.get_identifier()})'

    def trim(self) -> None:
        """Delete empty studies
        """
        for study in self.get_studies():
            study.trim()

        self.studies = list(filter(
            lambda s: not s.is_empty(), self.studies
        ))

    def is_empty(self) -> bool:
        """Check if studies is empty

        Returns
        -------
        bool
            True if patient has no instance
        """
        return self.studies == []
