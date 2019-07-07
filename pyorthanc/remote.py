# coding: utf-8
# author: gabriel couture
from typing import Dict

import requests

from pyorthanc import Orthanc


class RemoteModality:
    """Wrapper around Orthanc API when dealing with a (remote) modality.
    """

    def __init__(self, orthanc: Orthanc, modality: str) -> None:
        """Constructor

        Parameters
        ----------
        orthanc
            Orthanc object.
        modality
            Remote modality.
        """
        self.orthanc: Orthanc = orthanc
        self.modality: str = modality

    def echo(self) -> bool:
        """C-Echo to remote modality

        Returns
        -------
        bool
            True if C-Echo succeeded.
        """
        return self.orthanc.echo_to_modality(self.modality)

    def query(self, data: Dict) -> Dict:
        """C-Find (Querying with data)

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        requests.Response

        Examples
        -------
        >>> data = {'Level': 'Study',
        ...         'Query': {
        ...             'PatientID':'03HD*',
        ...             'StudyDescription':'*Chest*',
        ...             'PatientName':''
        ...         }
        ... }

        >>> remote_modality = RemoteModality(
        ...     orthanc=Orthanc('http://localhost:8042'),
        ...     modality='sample'
        ... )

        >>> remote_modality.query(data)
        """
        return self.orthanc.query_on_modality(self.modality, data=data)

    def move(self, data: Dict) -> requests.Response:
        """C-Move

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

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
        query_identifier
            Query identifier.
        target_modality
            Name of target modality (AET).

        Returns
        -------
        requests.Response

        Examples
        --------
        >>> remote_modality = RemoteModality(Orthanc('http://localhost:8042'), 'modality')
        >>> query_id = remote_modality.query(
        ...     data={'Level': 'Study',
        ...           'Query': {'QueryRetrieveLevel': 'Study',
        ...                     'Modality':'SR'}}).json()

        >>> remote_modality.retrieve(
        ...     query_identifier=query_id['ID'],
        ...     target_modality='modality'
        ... )

        """
        return self.orthanc.retrieve_query_results_to_given_modality(
            query_identifier, json=target_modality)
