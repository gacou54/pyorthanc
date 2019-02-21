# coding: utf-8
from typing import List, Dict

import requests
from requests import Response
from requests.auth import HTTPBasicAuth


class Orthanc:
    """Wrapper around Orthanc REST API

    You need to know if you need credentials before using this
    object. If yes, you need to set credentials with the method
    `setup_credential`.
    """

    def __init__(self, orthanc_url: str):
        """Constructor

        Parameters
        ----------
        orthanc_url : str
            Orthanc server address
        """
        self._orthanc_url: str = orthanc_url

        self._credentials_are_set: bool = False
        self._credentials: HTTPBasicAuth = None

    def setup_credentials(self, username: str, password: str) -> None:
        """Set credentials needed for HTTP requests

        Parameters
        ----------
        username : str
        password : str
        """
        self._credentials = HTTPBasicAuth(username, password)
        self._credentials_are_set = True

    def get_modalities(self) -> Response:
        """Get Orthanc modalities

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/modalities')

    def get_patients_identifiers(self) -> Response:
        """Get all Orthanc's patients identifiers

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/patients')

    def get_patient_information(self, patient_identifier: str) -> Response:
        """Get patient main information

        Parameters
        ----------
        patient_identifier : str
            Orthanc patient's identifier

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/patients/'
                                f'{patient_identifier}')

    def get_study_identifiers(self, patient_identifier: str) -> List[str]:
        """Get patient's study identifiers

        Parameters
        ----------
        patient_identifier : str
             Orthanc patient's identifier

        Returns
        -------
            List of patient's studies
        """
        patient_information: Dict = self.get_patient_information(patient_identifier).json()

        return patient_information['Studies']

    def get_study_information(self, study_identifier: str) -> Response:
        """Get study main information

        Parameters
        ----------
        study_identifier : str
            Orthanc study's identifier

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/studies/'
                                f'{study_identifier}')

    def get_series_identifiers(self, study_identifier: str) -> List[str]:
        """Get Studies's series identifiers

        Parameters
        ----------
        study_identifier : str
            Orthanc study's identifier

        Returns
        -------
            List of series identifiers
        """
        study_information: Dict = self.get_study_information(study_identifier).json()

        return study_information['Series']

    def get_series_information(self, series_identifier: str) -> Response:
        """Get series main information

        Parameters
        ----------
        series_identifier : str
            Orthanc series's identifier

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/series/'
                                f'{series_identifier}')

    def get_instance_identifiers(self, series_identifier: str) -> List[str]:
        """Get Series's instances identifiers

        Parameters
        ----------
        series_identifier : str
            Orthanc series's identifier

        Returns
        -------
        List[str]
            List of instances identifiers
        """
        series_information = self.get_series_information(series_identifier).json()

        return series_information['Instances']

    def get_instance_information(self, instance_identifier: str) -> Response:
        """Get instance's main information

        Parameters
        ----------
        instance_identifier : str
            Orthanc instance's identifier

        Returns
        -------
        requests.Response
        """
        return self.get_request(f'{self._orthanc_url}/instances/'
                                f'{instance_identifier}/simplified-tags')

    def retrieve_instance_dcm_file(self, instance_identifier: str) -> bytes:
        """Retrieve patient file under the form of bytes

        One way to write DICOM file from the returning bytes could be:
        >>> orthanc = Orthanc('ORTHANC_URL')
        >>> dicom_file_bytes = orthanc.retrieve_instance_dcm_file(instance_identifier)
        >>> with open('your_path', 'wb') as file_handler:
        ...     file_handler.write(dicom_file_bytes)

        Parameters
        ----------
        instance_identifier : str
            Orthanc instance identifier

        Returns
        -------
            Bytes corresponding to DICOM file
        """

        return self.get_request(f'{self._orthanc_url}/instances/'
                                f'{instance_identifier}/file').json()

    def get_request(self, route: str) -> requests.Response:
        """GET request with specified route

        Parameters
        ----------
        route : str

        Returns
        -------
        requests.Response
            Response of the HTTP GET requests
        """
        if self._credentials_are_set:
            return requests.get(route, auth=self._credentials)

        return requests.get(route)
