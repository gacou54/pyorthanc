# coding: utf-8
# author: gabriel couture
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(
        orthanc: Orthanc,
        max_nbr_workers: int = 100,
        series_filter: Callable = None,
        do_trim_forest_after_construction: bool = True) -> List[Patient]:
    """Build a patient forest

    Each tree in the forest correspond to a patient. The layers in the
    tree correspond to:

    ```Patient -> Studies -> Series -> Instances```

    Note that trees are build concurrently. You may want to change the
    default values. Increase this number could improve performance,
    but it will take more memory.

    Parameters
    ----------
    orthanc
        Orthanc object.
    max_nbr_workers
        Number of workers for to build the concurrent tree.
    series_filter
        Series filter (e.g. lambda series: series.get_modality() == 'SR')
    do_trim_forest_after_construction
        If True, trim the forest after its construction.

    Returns
    -------
    List[Patient]
        List of patient tree representation.
    """
    patient_identifiers = orthanc.get_patients().json()

    with ThreadPoolExecutor(max_workers=max_nbr_workers) as patient_executor:
        future_patients = patient_executor.map(
            lambda patient_identifier: _build_patient(
                patient_identifier,
                orthanc,
                series_filter
            ),
            patient_identifiers
        )

    patient_forest = list(future_patients)

    if do_trim_forest_after_construction:
        return trim_patient_forest(patient_forest)

    return patient_forest


def _build_patient(
        patient_identifier: str,
        orthanc: Orthanc,
        series_filter: Callable) -> Patient:
    study_information = orthanc.get_patient_study_information(patient_identifier).json()

    patient = Patient(patient_identifier, orthanc)
    patient.studies = [_build_study(i, orthanc, series_filter) for i in study_information]

    return patient


def _build_study(
        study_information: Dict,
        orthanc: Orthanc,
        series_filter: Callable) -> Study:
    series_information = orthanc.get_study_series_information(study_information['ID']).json()

    study = Study(study_information['ID'], orthanc, study_information)
    study.series = [_build_series(i, orthanc, series_filter) for i in series_information]

    return study


def _build_series(
        series_information: Dict,
        orthanc: Orthanc,
        series_filter: Callable) -> Series:
    instance_information = orthanc.get_series_instance_information(series_information['ID']).json()

    series = Series(series_information['ID'], orthanc, series_information)

    if series_filter is not None:
        if not series_filter(series):
            return series

    series.instances = [Instance(i['ID'], orthanc, i) for i in instance_information]

    return series


def trim_patient_forest(patient_forest: List[Patient]) -> List[Patient]:
    for patient in patient_forest:
        patient.trim()

    patients = filter(
        lambda patient: not patient.is_empty(), patient_forest
    )

    return list(patients)
