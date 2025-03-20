from typing import Any, Dict, List, Union

import httpx

from . import util
from ._find import _validate_level
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

    def echo(self) -> bool:
        """C-Echo to modality

        Returns
        -------
        bool
            True if C-Echo succeeded.
        """
        try:
            self.client.post_modalities_id_echo(self.modality)
            return True

        except httpx.HTTPError:
            return False

    def get(self, level: str, resources: Union[List[Dict[str, Any]], Dict[str, Any]]) -> Dict:
        """C-GET

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        level
            Level of the query ['Patient', 'Study', 'Series', 'Instance']
        resources
            Dict or list of dict of DICOM tags that identify data to retrieve,
            e.g. {'StudyInstanceUID': '1.3.6.1.4.1.22213.2.6291.2.1'}

        Returns
        -------
        Dict
            Orthanc Response (probably a Dictionary)

        Examples
        --------
        >>> modality = Modality(Orthanc('http://localhost:8042'), 'modality')
        >>> query_id = modality.get(
        ...     data={
        ...         'Level': 'Study',
        ...         'Resources': {'StudyInstanceUID': '1.3.6.1.4.1.22213.2.6291.2.1'}
        ...     }
        ... )

        """
        _validate_level(level)
        if isinstance(resources, dict):
            resources = [resources]

        return dict(self.client.post_modalities_id_get(self.modality, json={
            'Level': level,
            'Resources': resources
        }))

    def find(self, data: Dict) -> Dict:
        """C-Find (Querying with data)

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        Dict
            Returns a dictionary with the query ID and corresponding matches (i.e. answers) to the request
            {'ID': '<query_id>', 'answers': [{first match metadata}, {second math metadata}, ...]}

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

        >>> response = modality.find(data)
        >>> print(response['ID'], response['answers'])
        """
        query_id = self.client.post_modalities_id_query(self.modality, json=data)['ID']
        answers = self.get_query_answers(query_id)

        return {'ID': query_id, 'answers': answers}

    query = find  # Alias

    def move(self, query_identifier: str, cmove_data: Dict = None) -> Dict:
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

    def store(self, instance_or_series_id: str) -> Dict:
        """Store series or instance to modality.

        Parameters
        ----------
        instance_or_series_id
            Instance or Series Orthanc identifier.

        Returns
        -------
        Dict
            Information related to the C-Store operation.
        """
        return dict(self.client.post_modalities_id_store(
            self.modality,
            json=instance_or_series_id
        ))

    def get_query_answers(self, query_id: str, simplify: bool = True, short: bool = False) -> List[Dict]:
        """"""
        params = self._make_response_format_params(simplify=simplify, short=short)

        answers = []
        for answer_id in self.client.get_queries_id_answers(query_id):
            answer_content = self.client.get_queries_id_answers_index_content(query_id, answer_id, params)
            answers.append(answer_content)

        return answers

    def _make_response_format_params(self, simplify: bool, short: bool) -> Dict:
        if simplify and not short:
            params = {'simplify': True}
        elif short and not simplify:
            params = {'short': True}
        elif simplify and short:
            raise ValueError("simplify and short can't be both True.")
        else:
            params = {}

        return params


RemoteModality = Modality
