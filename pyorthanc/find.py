from typing import Dict, List, Union

from .client import Orthanc
from .instance import Instance
from .patient import Patient
from .series import Series
from .study import Study


def find_patients(orthanc: Orthanc,
                  query: Dict[str, str] = None,
                  labels: Union[list[str], str] = None,
                  labels_constraint: str = 'All') -> List[Patient]:
    return query_orthanc(
        orthanc,
        level='Patient',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_studies(orthanc: Orthanc,
                 query: Dict[str, str] = None,
                 labels: Union[list[str], str] = None,
                 labels_constraint: str = 'All') -> List[Study]:
    return query_orthanc(
        orthanc,
        level='Study',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_series(orthanc: Orthanc,
                query: Dict[str, str] = None,
                labels: Union[list[str], str] = None,
                labels_constraint: str = 'All') -> List[Series]:
    return query_orthanc(
        orthanc,
        level='Series',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def find_instances(orthanc: Orthanc,
                   query: Dict[str, str] = None,
                   labels: Union[list[str], str] = None,
                   labels_constraint: str = 'All') -> List[Instance]:
    return query_orthanc(
        orthanc,
        level='Instance',
        query=query,
        labels=labels,
        labels_constraint=labels_constraint
    )


def query_orthanc(orthanc: Orthanc,
                  level: str,
                  query: Dict[str, str] = None,
                  labels: Union[list[str], str] = None,
                  labels_constraint: str = 'All') -> List[Union[Patient, Study, Series, Instance]]:
    _validate_level(level)

    data = {
        'Expand': True,
        'Level': level,
        'Limit': LOOKUP_INTERVAL,
        'Since': 0,
        'Query': {}
    }

    if query is not None:
        data['Query'] = query

    if labels is not None:
        data['Labels'] = [labels] if isinstance(labels, str) else labels
        data['LabelsConstrain'] = labels_constraint

    results = []
    while True:
        result_for_interval = orthanc.post_tools_find(data)
        if len(result_for_interval) == 0:
            break

        results += result_for_interval
        data['Since'] += LOOKUP_INTERVAL  # Updating lookup window

    if level == 'Patient':
        return [Patient(i['ID'], orthanc, i) for i in results]

    if level == 'Study':
        return [Study(i['ID'], orthanc, i) for i in results]

    if level == 'Series':
        return [Series(i['ID'], orthanc, i) for i in results]

    if level == 'Instance':
        return [Instance(i['ID'], orthanc, i) for i in results]


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


LOOKUP_INTERVAL = 1_000
