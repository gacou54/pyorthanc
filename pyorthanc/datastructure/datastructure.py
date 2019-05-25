# coding: utf-8
# author: gabriel couture
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Generator

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(orthanc: Orthanc, max_worker: int = 100) -> List[Patient]:
    """Build a patient forest

    Each tree in the forest correspond to a patient. The layers in the
    tree correspond to:
        Patient -> Studies -> Series -> Instance

    Note that trees are build asynchronously. You may want to change the
    default value (100). Increase this number could improve performance,
    but it will take more memory.

    Parameters
    ----------
    orthanc : Orthanc object.
    max_worker : Number of maximum workers for the concurrent building tree.

    Returns
    -------
    List[Patient]
        List of patient tree representation.
    """
    event_loop = asyncio.get_event_loop()

    return event_loop.run_until_complete(_build_patient_forest(orthanc, max_worker))


async def _build_patient_forest(orthanc: Orthanc, max_worker: int) -> List[Patient]:
    nbr_patient_workers = int(max_worker / 2) if int(max_worker / 2) != 0 else 1
    nbr_study_workers = int(max_worker / 8) if int(max_worker / 8) != 0 else 1
    nbr_series_workers = int(max_worker / 8) if int(max_worker / 8) != 0 else 1
    nbr_instance_workers = int(max_worker / 4) if int(max_worker / 4) != 0 else 1

    patient_identifiers: List[str] = orthanc.get_patients().json()

    with ThreadPoolExecutor(max_workers=nbr_patient_workers) as patient_executor:
        with ThreadPoolExecutor(max_workers=nbr_study_workers) as study_executor:
            with ThreadPoolExecutor(max_workers=nbr_series_workers) as series_executor:
                with ThreadPoolExecutor(max_workers=nbr_instance_workers) as instance_executor:
                    patients: Generator = patient_executor.map(
                        lambda patient_identifier:
                            _build_patient(
                                patient_identifier,
                                orthanc,
                                study_executor,
                                series_executor,
                                instance_executor
                            ),
                        patient_identifiers
                    )

    patients = list(patients)
    print(patients)
    return patients


def _build_patient(
        patient_identifier: str,
        orthanc: Orthanc,
        study_executor: ThreadPoolExecutor,
        series_executor: ThreadPoolExecutor,
        instance_executor: ThreadPoolExecutor) -> Patient:
    study_identifiers = orthanc.get_patient_studies(patient_identifier).json()

    patient = Patient(patient_identifier, orthanc)
    patient.studies = study_executor.map(
        lambda study_identifier: _build_study(
                study_identifier,
                orthanc,
                series_executor,
                instance_executor
        ),
        study_identifiers
    )
    print('study')

    return patient


def _build_study(
        study_identifier: str,
        orthanc: Orthanc,
        series_executor: ThreadPoolExecutor,
        instance_executor: ThreadPoolExecutor) -> Study:
    series_identifiers = orthanc.get_study_series_identifiers(study_identifier).json()

    study = Study(study_identifier, orthanc)
    study.studies = series_executor.map(
        lambda series_identifier: _build_series(
                series_identifier,
                orthanc,
                instance_executor
        ),
        series_identifiers
    )

    return study


def _build_series(
        series_identifier: str,
        orthanc: Orthanc,
        instance_executor: ThreadPoolExecutor) -> Series:
    instance_identifiers = orthanc.get_series_instances(series_identifier).json()

    series = Series(series_identifier, orthanc)
    series.instances = instance_executor.map(
        lambda instance_identifier: Instance(instance_identifier, orthanc),
        instance_identifiers
    )

    return series

