from typing import Dict, List, Union

from pyorthanc.resources.instance import Instance
from pyorthanc.resources.patient import Patient
from pyorthanc.resources.series import Series
from pyorthanc.resources.study import Study
from .client import Orthanc

DEFAULT_RESOURCES_LIMIT = 1_000


def find_patients(client: Orthanc,
                  query: Dict[str, str] = None,
                  labels: Union[list[str], str] = None,
                  labels_constraint: str = 'All') -> List[Patient]:
    return query_orthanc(
        client=client,
        level='Patient',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_studies(client: Orthanc,
                 query: Dict[str, str] = None,
                 labels: Union[list[str], str] = None,
                 labels_constraint: str = 'All') -> List[Study]:
    return query_orthanc(
        client=client,
        level='Study',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_series(client: Orthanc,
                query: Dict[str, str] = None,
                labels: Union[list[str], str] = None,
                labels_constraint: str = 'All') -> List[Series]:
    return query_orthanc(
        client=client,
        level='Series',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_instances(client: Orthanc,
                   query: Dict[str, str] = None,
                   labels: Union[list[str], str] = None,
                   labels_constraint: str = 'All') -> List[Instance]:
    return query_orthanc(
        client=client,
        level='Instance',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def query_orthanc(client: Orthanc,
                  level: str,
                  query: Dict[str, str] = None,
                  labels: Union[list[str], str] = None,
                  labels_constraint: str = 'All',
                  limit: int = DEFAULT_RESOURCES_LIMIT,
                  since: int = 0,
                  retrieve_all_resources: bool = True) -> List[Union[Patient, Study, Series, Instance]]:
    _validate_level(level)
    _validate_labels_constraint(labels_constraint)

    data = {
        'Expand': True,
        'Level': level,
        'Limit': limit,
        'Since': since,
        'Query': {}
    }

    if query is not None:
        data['Query'] = query

    if labels is not None:
        data['Labels'] = [labels] if isinstance(labels, str) else labels
        data['LabelsConstraint'] = labels_constraint

    if retrieve_all_resources:
        results = []
        while True:
            result_for_interval = client.post_tools_find(data)
            if len(result_for_interval) == 0:
                break

            results += result_for_interval
            data['Since'] += limit  # Updating the lookup window
    else:
        results = client.post_tools_find(data)

    if level == 'Patient':
        return [Patient(i['ID'], client, i) for i in results]

    if level == 'Study':
        return [Study(i['ID'], client, i) for i in results]

    if level == 'Series':
        return [Series(i['ID'], client, i) for i in results]

    if level == 'Instance':
        return [Instance(i['ID'], client, i) for i in results]


def _validate_labels_constraint(labels_constraint: str) -> None:
    if labels_constraint not in ['All', 'Any', 'None']:
        raise ValueError(
            "labels_constraint should be one of ['All', 'Any', 'None'], "
            f"got {labels_constraint} instead."
        )


def _validate_level(level: str) -> None:
    if level not in ['Patient', 'Study', 'Series', 'Instance']:
        raise ValueError(
            "level should be one of ['Patient', 'Study', 'Series', 'Instance'], "
            f"got {level} instead."
        )
