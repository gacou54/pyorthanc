from typing import Dict, List, Optional, Union

import httpx

from . import util
from .client import Orthanc


class Modality:
    """Wrapper around Orthanc API when dealing with a modality."""

    def __init__(self, client: Orthanc, modality: str) -> None:
        """Constructor

        Parameters
        ----------
        client
            Orthanc object.
        modality
            Remote modality.
        """
        client = util.ensure_non_raw_response(client)

        self.client = client
        self.modality = modality

    def echo(self, check_find: Optional[bool] = None, timeout: Optional[int] = None) -> bool:
        """C-Echo to modality

        Parameters
        ----------
        check_find
            Issue a dummy C-FIND command after the C-GET SCU, in order to check whether the remote modality
            knows about Orthanc. This field defaults to the value of the `DicomEchoChecksFind` configuration option.
            New in Orthanc 1.8.1.
        timeout
            Timeout for the C-ECHO command, in seconds. The default value is the `DicomScuTimeout` in the configuration.
            If `timeout` is set to 0, this means no timeout.
        Returns
        -------
        bool
            True if C-Echo succeeded.
        """
        data = {}
        if check_find is not None:
            data['CheckFind'] = check_find
        if timeout is not None:
            data['Timeout'] = timeout

        try:
            self.client.post_modalities_id_echo(id_=self.modality, json=data)
            return True

        except httpx.HTTPError:
            return False

    def query(self, data: Dict) -> Dict:
        """C-Find (Querying with data)

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        Dict
            Dictionary with keys {'ID': '...', 'path': '...'}

        Examples
        -------
        >>> data = {'Level': 'Study',
        ...         'Query': {
        ...             'PatientID':'03HD*',
        ...             'StudyDescription':'*Chest*',
        ...             'PatientName':''
        ...         }
        ... }

        >>> modality = Modality(
        ...     client=Orthanc('http://localhost:8042'),
        ...     modality='sample'
        ... )

        >>> modality.query(data)
        """
        return dict(self.client.post_modalities_id_query(self.modality, json=data))

    def move(self, query_identifier: str, cmove_data: Dict) -> Dict:
        """C-Move query results to another modality

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        query_identifier
            Query identifier.
        cmove_data
            Ex. {'TargetAet': 'target_modality_name', "Synchronous": False}

        Returns
        -------
        Dict
            Orthanc Response (probably a Dictionary)

        Examples
        --------
        >>> modality = Modality(Orthanc('http://localhost:8042'), 'modality')
        >>> query_id = modality.query(
        ...     data={'Level': 'Series',
        ...           'Query': {'PatientID': '',
        ...                     'Modality':'SR'}})

        >>> modality.move(
        ...     query_identifier=query_id['ID'],
        ...     cmove_data={'TargetAet': 'TARGETAET'}
        ... )

        """
        return dict(self.client.post_queries_id_retrieve(query_identifier, json=cmove_data))

    def store(self, resource_ids: Union[str, List[str]]) -> Dict:
        """Store a resource to modality (C-Store).

        Parameters
        ----------
        resource_ids
            Orthanc resource identifier to store to the modality.

        Returns
        -------
        Dict
            Information related to the C-Store operation.
        """
        return dict(self.client.post_modalities_id_store(
            self.modality,
            json=resource_ids
        ))

    def get_query_answers(self) -> Dict:
        answers = {}

        for query_id in self.client.get_queries():
            for answer_id in self.client.get_queries_id_answers(query_id):
                answers[query_id] = self.client.get_queries_id_answers_index_content(query_id, answer_id)

        return answers


RemoteModality = Modality
