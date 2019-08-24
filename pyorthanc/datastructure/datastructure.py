# coding: utf-8
# author: gabriel couture
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Optional

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


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

    if do_trim_forest_after_construction:
        return trim_patient_forest(patient_forest)

    return patient_forest


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


def retrieve_and_write_patients_forest_to_given_path(
        patient_forest: List[Patient],
        path: str) -> None:
    """Retrieve and write patients to given path

    Parameters
    ----------
    patient_forest
        Patient forest.
    path
        Path where you want to write the files.
    """
    anonymized_patient_counter = 1
    for patient in patient_forest:

        if patient.get_id().strip() == '':
            patient_path = os.path.join(path, f'anonymized-patient-{anonymized_patient_counter}')
            anonymized_patient_counter += 1
        else:
            patient_path = os.path.join(path, patient.get_id())

        used_study_paths: List[str] = []  # Sometime there are many studies with the same "ID" name.

        for j, study in enumerate(patient.get_studies()):
            study_path = os.path.join(patient_path, 'anonymized-study' if study.get_id() == '' else study.get_id())

            if study_path in used_study_paths:
                study_path += str(j + 1)
            used_study_paths.append(study_path)

            os.makedirs(study_path, exist_ok=True)

            for series in study.get_series():
                for k, instance in enumerate(series.get_instances()):
                    instance_path = os.path.join(study_path, f'{series.get_modality()}-{k+1}.dcm')

                    dicom_file_bytes = instance.get_dicom_file_content()
                    with open(instance_path, 'wb') as file_handler:
                        file_handler.write(dicom_file_bytes)
