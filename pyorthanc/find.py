from typing import Dict, List, Union

from .client import Orthanc
from .resources.instance import Instance
from .resources.patient import Patient
from .resources.resource import Resource
from .resources.series import Series
from .resources.study import Study

DEFAULT_RESOURCES_LIMIT = 1_000


def find_patients(client: Orthanc,
                  query: Dict[str, str] = None,
                  labels: Union[list[str], str] = None,
                  labels_constraint: str = 'All') -> List[Patient]:
    """Finds patients in Orthanc according to queries and labels

    Parameters
    ----------
    client
        Orthanc client.
    query
        Dictionary that specifies the filters on the Patient related DICOM tags.
    labels
        List of strings specifying which labels to look for in the resources.
    labels_constraint
        Constraint on the labels, can be 'All', 'Any', or 'None'.

    Returns
    -------
    List[Patient]
        List of patients that fit the provided criteria.

    Examples
    --------
    ```python
    import pyorthanc

    client = pyorthanc.Orthanc('http://localhost:8042', 'orthanc', 'orthanc')
    patients = find_patients(
        client=client,
        query={'PatientID': 'Something*'},
        labels=['my_label']
    )
    ```
    """
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
    """Finds studies in Orthanc according to queries and labels

    Parameters
    ----------
    client
        Orthanc client.
    query
        Dictionary that specifies the filters on the Study related DICOM tags.
    labels
        List of strings specifying which labels to look for in the resources.
    labels_constraint
        Constraint on the labels, can be 'All', 'Any', or 'None'.

    Returns
    -------
    List[Study]
        List of studies that fit the provided criteria.

    Examples
    --------
    ```python
    import pyorthanc

    client = pyorthanc.Orthanc('http://localhost:8042', 'orthanc', 'orthanc')
    studies = find_studies(
        client=client,
        query={'ReferringPhysicianName': 'Something*'},
        labels=['my_label']
    )
    ```
    """

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
    """Finds series in Orthanc according to queries and labels

    Parameters
    ----------
    client
        Orthanc client.
    query
        Dictionary that specifies the filters on the Series related DICOM tags.
    labels
        List of strings specifying which labels to look for in the resources.
    labels_constraint
        Constraint on the labels, can be 'All', 'Any', or 'None'.

    Returns
    -------
    List[Series]
        List of Series that fit the provided criteria.

    Examples
    --------
    ```python
    import pyorthanc

    client = pyorthanc.Orthanc('http://localhost:8042', 'orthanc', 'orthanc')
    series = find_series(
        client=client,
        query={'Modality': 'RTDose'},
        labels=['my_label']
    )
    ```
    """
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
    """Finds instances in Orthanc according to queries and labels

    Parameters
    ----------
    client
        Orthanc client.
    query
        Dictionary that specifies the filters on the instances related DICOM tags.
    labels
        List of strings specifying which labels to look for in the resources.
    labels_constraint
        Constraint on the labels, can be 'All', 'Any', or 'None'.

    Returns
    -------
    List[Instance]
        List of Instances that fit the provided criteria.

    Examples
    --------
    ```python
    import pyorthanc

    client = pyorthanc.Orthanc('http://localhost:8042', 'orthanc', 'orthanc')
    instances = find_instances(
        client=client,
        query={'InstanceCreationDate': '20100301'},
        labels=['my_label']
    )
    ```
    """
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
                  retrieve_all_resources: bool = True) -> List[Resource]:
    """

    Parameters
    ----------
    client
        Orthanc client.
    level
        Level of the query ['Patient', 'Study', 'Series', 'Instance'].
    query
        Dictionary that specifies the filters on the level related DICOM tags.
    labels
        List of strings specifying which labels to look for in the resources.
    labels_constraint
        Constraint on the labels, can be 'All', 'Any', or 'None'.
    limit
        Limit the number of reported resources.
    since
        Show only the resources since the provided index (in conjunction with "limit").
    retrieve_all_resources
        Retrieve all resources since the index specified in the "since" parameter.

    Returns
    -------
    List[Resource]
        List of resources that fit the provided criteria.

    Examples
    --------
    ```python
    import pyorthanc

    client = pyorthanc.Orthanc('http://localhost:8042', 'orthanc', 'orthanc')
    instances = query_orthanc(
        client=client,
        level='Instance',
        query={'InstanceCreationDate': '20100301'},
        labels=['my_label'],
        since=100,
        retrieve_all_resource=False
    )
    """
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
