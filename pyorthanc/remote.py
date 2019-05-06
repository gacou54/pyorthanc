# coding: utf-8
# author: gabriel couture
from typing import Dict

import requests
from requests.auth import HTTPBasicAuth

from pyorthanc import Orthanc


class RemoteModality:
    """Wrapper around Orthanc API when dealing with a (remote) modality.
    """

    def __init__(self, orthanc_url: str, modality: str) -> None:
        """Constructor

        Parameters
        ----------
        orthanc_url : str
        modality : str
        """
        self.orthanc: Orthanc = Orthanc(orthanc_url)
        self.modality: str = modality

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

    def echo(self) -> requests.Response:
        """C-Echo to remote modality

        Returns
        -------
        requests.Response
            Response object from echo.
        """
        return self.orthanc.echo_to_modality(self.modality)

    def query(self, data: Dict) -> requests.Response:
        """C-Find (Querying with data)

        Parameters
        ----------
        data : Dictionary to send in the body of request.

        Returns
        -------
        requests.Response

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
        """
        return self.orthanc.query_on_modality(self.modality, data=data)

    def move(self, data: Dict) -> requests.Response:
        """C-Move

        Parameters
        ----------
        data : Dictionary to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.orthanc.move_from_modality(self.modality, data=data)

    def retrieve(self, query_identifier: str, target_modality: str,) -> requests.Response:
        """Retrieve (C-Move) query results to another modality

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        query_identifier : Query identifier.
        target_modality : Name of target modality (AET).

        Returns
        -------
        requests.Response

        Examples
        --------
        >>> remote_modality = RemoteModality('http://localhost:8042', 'modality')
        >>> query_id = remote_modality.query(
        ...     data={'Level': 'Study',
        ...           'Query': {'QueryRetrieveLevel': 'Study',
        ...                     'Modality':'SR'}}).json()

        >>> remote_modality.retrieve(query_identifier=query_id['ID'],
        ...                          target_modality='modality')

        """
        return self.orthanc.retrieve_query_results_to_another_modality(
            query_identifier, json=target_modality)

