# coding: utf-8
# author: gabriel couture
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(
        orthanc: Orthanc,
        nbr_patient_workers: int = 100,
        nbr_study_workers: int = 10,
        nbr_series_workers: int = 10,
        nbr_instance_workers: int = 100) -> List[Patient]:
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
    nbr_patient_workers
        Number of patient workers for the concurrent building tree.
    nbr_study_workers
        Number of study workers for the concurrent building tree.
    nbr_series_workers
        Number of series workers for the concurrent building tree.
    nbr_instance_workers
        Number of instance workers for the concurrent building tree.

    Returns
    -------
    List[Patient]
        List of patient tree representation.
    """
    patient_identifiers = orthanc.get_patients().json()
    with ThreadPoolExecutor(max_workers=nbr_patient_workers) as patient_executor:
        with ThreadPoolExecutor(max_workers=nbr_study_workers) as study_executor:
            with ThreadPoolExecutor(max_workers=nbr_series_workers) as series_executor:
                with ThreadPoolExecutor(max_workers=nbr_instance_workers) as instance_executor:
                    future_patients = patient_executor.map(
                            lambda patient_identifier: _build_patient(
                                patient_identifier,
                                orthanc,
                                study_executor,
                                series_executor,
                                instance_executor
                            ),
                            patient_identifiers
                        )

    return list(future_patients)


def _build_patient(
        patient_identifier: str,
        orthanc: Orthanc,
        study_executor: ThreadPoolExecutor,
        series_executor: ThreadPoolExecutor,
        instance_executor: ThreadPoolExecutor) -> Patient:
    study_information = orthanc.get_patient_study_information(patient_identifier).json()
    study_identifiers = [study['ID'] for study in study_information]

    patient = Patient(patient_identifier, orthanc)
    future_studies = study_executor.map(
        lambda study_identifier: _build_study(
            study_identifier,
            orthanc,
            series_executor,
            instance_executor
        ),
        study_identifiers
    )

    patient.studies = list(future_studies)

    return patient


def _build_study(
        study_identifier: str,
        orthanc: Orthanc,
        series_executor: ThreadPoolExecutor,
        instance_executor: ThreadPoolExecutor) -> Study:
    series_information = orthanc.get_study_series_information(study_identifier).json()
    series_identifiers = [series['ID'] for series in series_information]

    study = Study(study_identifier, orthanc)
    future_series = series_executor.map(
        lambda series_identifier: _build_series(
            series_identifier,
            orthanc,
            instance_executor
        ),
        series_identifiers
    )

    study.series = list(future_series)

    return study


def _build_series(
        series_identifier: str,
        orthanc: Orthanc,
        instance_executor: ThreadPoolExecutor) -> Series:
    instance_information = orthanc.get_series_instance_information(series_identifier).json()
    instance_identifiers = [instance['ID'] for instance in instance_information]

    series = Series(series_identifier, orthanc)
    future_instances = instance_executor.map(
        lambda instance_identifier: Instance(instance_identifier, orthanc),
        instance_identifiers
    )

    series.instances = list(future_instances)

    return series
