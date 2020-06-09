# coding: utf-8
# author: gabriel couture
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Optional

from pyorthanc import Study, Series, Instance
from pyorthanc.orthanc import Orthanc
from pyorthanc.patient import Patient


def build_patient_forest(
        orthanc: Orthanc,
        max_nbr_workers: int = 100,
        patient_filter: Optional[Callable] = None,
        study_filter: Optional[Callable] = None,
        series_filter: Optional[Callable] = None,
        do_trim_forest_after_construction: bool = True) -> List[Patient]:
    """Build a patient forest

    Each tree in the forest correspond to a patient. The layers in the
    tree correspond to:

    `Patient -> Studies -> Series -> Instances`

    Note that trees are build concurrently. You may want to change the
    default values. Increase this number could improve performance,
    but it will take more memory.

    Parameters
    ----------
    orthanc
        Orthanc object.
    max_nbr_workers
        Number of workers for to build the concurrent tree.
    patient_filter
        Patient filter (e.g. lambda patient: patient.get_id() == '03HDQ99*')
    study_filter
        Study filter (e.g. lambda study: study.get_id() == '*pros*')
    series_filter
        Series filter (e.g. lambda series: series.get_modality() == 'SR')
    do_trim_forest_after_construction
        If True, trim the forest after its construction.

    Returns
    -------
    List[Patient]
        List of patient tree representation.
    """
    patient_identifiers = orthanc.get_patients()

    with ThreadPoolExecutor(max_workers=max_nbr_workers) as patient_executor:
        future_patients = patient_executor.map(
            lambda patient_identifier: _build_patient(
                patient_identifier,
                orthanc,
                patient_filter,
                study_filter,
                series_filter
            ),
            patient_identifiers
        )

    patient_forest = list(future_patients)

    return trim_patient_forest(patient_forest) if do_trim_forest_after_construction else patient_forest


def _build_patient(
        patient_identifier: str,
        orthanc: Orthanc,
        patient_filter: Optional[Callable],
        study_filter: Optional[Callable],
        series_filter: Optional[Callable]) -> Patient:
    study_information = orthanc.get_patient_studies_information(patient_identifier)

    patient = Patient(patient_identifier, orthanc)

    if patient_filter is not None:
        if not patient_filter(patient):
            return patient

    patient.studies = [_build_study(i, orthanc, study_filter, series_filter) for i in study_information]

    return patient


def _build_study(
        study_information: Dict,
        orthanc: Orthanc,
        study_filter: Optional[Callable],
        series_filter: Optional[Callable]) -> Study:
    series_information = orthanc.get_study_series_information(study_information['ID'])

    study = Study(study_information['ID'], orthanc, study_information)

    if study_filter is not None:
        if not study_filter(study):
            return study

    study.series = [_build_series(i, orthanc, series_filter) for i in series_information]

    return study


def _build_series(
        series_information: Dict,
        orthanc: Orthanc,
        series_filter: Optional[Callable]) -> Series:
    instance_information = orthanc.get_series_instance_information(series_information['ID'])

    series = Series(series_information['ID'], orthanc, series_information)

    if series_filter is not None:
        if not series_filter(series):
            return series

    series.instances = [Instance(i['ID'], orthanc, i) for i in instance_information]

    return series


def trim_patient_forest(patient_forest: List[Patient]) -> List[Patient]:
    """Trim Patient forest (list of patients)

    Parameters
    ----------
    patient_forest
        Patient forest.

    Returns
    -------
    List[Patient]
        Pruned patient forest.
    """
    for patient in patient_forest:
        patient.trim()

    patients = filter(
        lambda p: not p.is_empty(), patient_forest
    )

    return list(patients)


def retrieve_and_write_patients(patient_forest: List[Patient], path: str) -> None:
    """Retrieve and write patients to given path

    Parameters
    ----------
    patient_forest
        Patient forest.
    path
        Path where you want to write the files.
    """
    os.makedirs(path, exist_ok=True)
    for patient in patient_forest:
        retrieve_patient(patient, path)


def retrieve_patient(patient: Patient, path: str) -> None:
    patient_path = _make_patient_path(path, patient.get_id())
    os.makedirs(patient_path, exist_ok=True)

    for study in patient.get_studies():
        retrieve_study(study, patient_path)


def retrieve_study(study: Study, patient_path: str) -> None:
    study_path = _make_study_path(patient_path, study.get_id())
    os.makedirs(study_path, exist_ok=True)

    for series in study.get_series():
        retrieve_series(series, study_path)


def retrieve_series(series: Series, study_path: str) -> None:
    series_path = _make_series_path(study_path, series.get_modality())
    os.makedirs(series_path, exist_ok=True)

    for instance in series.get_instances():
        retrieve_instance(instance, series_path)


def retrieve_instance(instance: Instance, series_path) -> None:
    path = os.path.join(series_path, instance.get_uid() + '.dcm')

    dicom_file_bytes = instance.get_dicom_file_content()

    with open(path, 'wb') as file_handler:
        file_handler.write(dicom_file_bytes)


def _make_patient_path(path: str, patient_id: str) -> str:
    patient_directories = os.listdir(path)

    if patient_id.strip() == '':
        patient_id = 'anonymous-patient'
        return os.path.join(path, _make_path_name(patient_id, patient_directories))

    return os.path.join(path, patient_id)


def _make_study_path(patient_path: str, study_id: str) -> str:
    study_directories = os.listdir(patient_path)

    if study_id.strip() == '':
        study_id = 'anonymous-study'

    return os.path.join(patient_path, _make_path_name(study_id, study_directories))


def _make_series_path(study_path: str, modality: str) -> str:
    series_directories = os.listdir(study_path)

    return os.path.join(study_path, _make_path_name(modality, series_directories))


def _make_path_name(name: str, directories: List[str], increment: int = 1, has_increment: bool = False) -> str:
    if not has_increment:
        name = f'{name}-{increment}'
        has_increment = True
    else:
        name = '-'.join(name.split('-')[:-1])

    if name in directories:
        return _make_path_name(name, directories, increment + 1, has_increment)

    return name
