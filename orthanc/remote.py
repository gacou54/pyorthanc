# coding: utf-8
# author: gabriel couture
from typing import Dict, Any

import requests
from requests.auth import HTTPBasicAuth


class RemoteModality:
    """Wrapper around Orthanc API when dealing with a remote modality.
    """

    def __init__(self, orthanc_url: str, modality: str):
        """Constructor

        Parameters
        ----------
        orthanc_url : str
        modality : str
        """
        self.orthanc_url: str = orthanc_url
        self.modality: str = modality

        self.credentials_are_set: bool = False
        self.credentials: HTTPBasicAuth = None

    def setup_credentials(self, username: str, password: str) -> None:
        """Set credentials needed for HTTP requests

        Parameters
        ----------
        username : str
        password : str
        """
        self.credentials = HTTPBasicAuth(username, password)
        self.credentials_are_set = True

    def echo(self) -> requests.Response:
        """C-Echo to remote modality

        Returns
        -------
        requests.Response
            Response object from echo.
        """
        return self.post_request(f'{self.orthanc_url}/modalities/{self.modality}/echo')

    def query(self, data: Dict) -> requests.Response:
        """C-Find (Querying with data)

        Examples
        -------
        >>> data = {'Level': 'Study',
        ...         'Query': {'PatientID':'03HD*',
        ...                   'StudyDescription':'*Chest*',
        ...                   'PatientName':''
        ...                  }
        ... }

        >>> remote_modality = RemoteModality(orthanc_url='http://localhost:8042',
        ...                                  modality='sample')

        >>> remote_modality.setup_credentials('username', 'password')
        >>> remote_modality.query(data=data)

        Parameters
        ----------
        data : dict
            Data dictionary.

        Returns
        -------
        requests.Response
        """
        formatted_data = self.__format_data(data)

        return self.post_request(f'{self.orthanc_url}/modalities/'
                                 f'{self.modality}/query',
                                 data=formatted_data)

    def move(self, data: Dict) -> requests.Response:
        """C-Move

        Returns
        -------
        requests.Response
        """
        formatted_data = self.__format_data(data)

        return self.post_request(f'{self.orthanc_url}/modalities/'
                                 f'{self.modality}/move',
                                 data=formatted_data)

    def post_request(self, route: str, data: str = None) -> Any:
        """POST to specified route

        Parameters
        ----------
        route : str
        data : dict
            Dictionary of data for the POST HTTP request

        Returns
        -------
        requests.Response
            Response of the HTTP POST requests
        """
        if self.credentials_are_set:
            return requests.post(route, data=data, auth=self.credentials)

        return requests.post(route, data=data)

    def __format_data(self, data: Dict) -> str:
        """Format dictionary data in a string

        Parameters
        ----------
        data: Dict
            Data dictionary

        Returns
        -------
        str
            String corresponding to data
        """
        return str(data).replace('\'', '\"')
