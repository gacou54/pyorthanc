from typing import Dict, List, Union

from . import util
from ._resources.instance import Instance
from ._resources.patient import Patient
from ._resources.resource import Resource
from ._resources.series import Series
from ._resources.study import Study
from .client import Orthanc

DEFAULT_RESOURCES_LIMIT = 1_000


def find_patients(client: Orthanc,
                  query: Dict[str, str] = None,
                  labels: Union[List[str], str] = None,
                  labels_constraint: str = 'All',
                  **kwargs) -> List[Patient]:
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
    **kwargs
        Additional keyword arguments passed to `query_orthanc`

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
        labels_constraint=labels_constraint,
        **kwargs
    )


def find_studies(client: Orthanc,
                 query: Dict[str, str] = None,
                 labels: Union[List[str], str] = None,
                 labels_constraint: str = 'All',
                 **kwargs) -> List[Study]:
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
    **kwargs
        Additional keyword arguments passed to `query_orthanc`

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
        labels_constraint=labels_constraint,
        **kwargs
    )


def find_series(client: Orthanc,
                query: Dict[str, str] = None,
                labels: Union[List[str], str] = None,
                labels_constraint: str = 'All',
                **kwargs) -> List[Series]:
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
    **kwargs
        Additional keyword arguments passed to `query_orthanc`

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
        labels_constraint=labels_constraint,
        **kwargs
    )


def find_instances(client: Orthanc,
                   query: Dict[str, str] = None,
                   labels: Union[List[str], str] = None,
                   labels_constraint: str = 'All',
                   **kwargs) -> List[Instance]:
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
    **kwargs
        Additional keyword arguments passed to `query_orthanc`

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
        labels_constraint=labels_constraint,
        **kwargs
    )


def query_orthanc(client: Orthanc,
                  level: str,
                  query: Dict[str, str] = None,
                  labels: Union[List[str], str] = None,
                  labels_constraint: str = 'All',
                  limit: int = DEFAULT_RESOURCES_LIMIT,
                  since: int = 0,
                  retrieve_all_resources: bool = True,
                  lock_children: bool = False) -> List[Resource]:
    """Query data in the Orthanc server

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
    lock_children
        If `lock_children` is True, the resource children (ex. instances of a series via `Series.instances`)
        will be cached at the first query rather than queried every time. This is useful when you want
        to filter the children of a resource and want to maintain the filter result.
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
    ```
    """
    _validate_level(level)
    _validate_labels_constraint(labels_constraint)

    # In this function, client that return raw responses are not supported.
    client = util.ensure_non_raw_response(client)

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
        resources = [Patient(i['ID'], client, _lock_children=lock_children) for i in results]
    elif level == 'Study':
        resources = [Study(i['ID'], client, _lock_children=lock_children) for i in results]
    elif level == 'Series':
        resources = [Series(i['ID'], client, _lock_children=lock_children) for i in results]
    elif level == 'Instance':
        resources = [Instance(i['ID'], client, _lock_children=lock_children) for i in results]
    else:
        raise ValueError(f"Unknown level ['Patient', 'Study', 'Series', 'Instance'], got {level}")

    return resources


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
