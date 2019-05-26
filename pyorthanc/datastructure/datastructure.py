# coding: utf-8
# author: gabriel couture
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(
        orthanc: Orthanc,
        max_nbr_workers: int = 100) -> List[Patient]:
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
                orthanc
            ),
            patient_identifiers
        )

    return list(future_patients)


def _build_patient(patient_identifier: str, orthanc: Orthanc) -> Patient:
    study_information = orthanc.get_patient_study_information(patient_identifier).json()

    patient = Patient(patient_identifier, orthanc)
    patient.studies = [_build_study(i, orthanc, ) for i in study_information]

    return patient


def _build_study(study_information: Dict, orthanc: Orthanc) -> Study:
    series_information = orthanc.get_study_series_information(study_information['ID']).json()

    study = Study(study_information['ID'], orthanc, study_information)
    study.series = [_build_series(i, orthanc) for i in series_information]

    return study


def _build_series(series_information: Dict, orthanc: Orthanc) -> Series:
    instance_information = orthanc.get_series_instance_information(series_information['ID']).json()

    series = Series(series_information['ID'], orthanc, series_information)
    series.instances = [Instance(i['ID'], orthanc, i) for i in instance_information]

    return series
