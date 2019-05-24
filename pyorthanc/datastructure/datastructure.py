# coding: utf-8
# author: gabriel couture
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from pyorthanc.datastructure.tree import Study
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
    patient_identifiers: List[str] = orthanc.get_patients().json()

    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        event_loop = asyncio.get_event_loop()

        futures = [
            event_loop.run_in_executor(
                executor,
                lambda patient_identifier: _build_patient(patient_identifier, orthanc, executor),
                patient_identifier
            )
            for patient_identifier in patient_identifiers
        ]

        responses = [r for r in await asyncio.gather(*futures)]

    return responses


async def _build_patient(patient_identifier: str, orthanc: Orthanc, executor: ThreadPoolExecutor) -> Patient:
    study_identifiers = orthanc.get_patient_studies(patient_identifier).json()

    event_loop = asyncio.get_event_loop()

    futures = [
        event_loop.run_in_executor(
            executor,
            lambda study_identifier: _build_study(study_identifier, orthanc),
            study_identifier
        )
        for study_identifier in study_identifiers
    ]

    patient = Patient(patient_identifier, orthanc)
    patient.studies = [r for r in await asyncio.gather(*futures)]

    return patient


async def _build_study(study_identifier: str, orthanc: Orthanc, executor: ThreadPoolExecutor) -> Study:
    series_identifiers = orthanc.get_study_series_identifiers(study_identifier).json()

    event_loop = asyncio.get_event_loop()

    futures = [
        event_loop.run_in_executor(
            executor,
            lambda series_identifier: _build_study(series_identifier, orthanc),
            series_identifier
        )
        for series_identifier in series_identifiers
    ]

    study = Study(study_identifier, orthanc)
    study.series = [r for r in await asyncio.gather(*futures)]

    return study

