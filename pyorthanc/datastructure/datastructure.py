# coding: utf-8
# author: gabriel couture
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from pyorthanc.datastructure.tree import Study, Series, Instance
from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(orthanc: Orthanc, max_worker: int = 100) -> List[Patient]:
    """Build a patient forest

    Each tree in the forest correspond to a patient. The layers in the
    tree correspond to:

    ```Patient -> Studies -> Series -> Instances```

    Note that trees are build asynchronously. You may want to change the
    default value (100). Increase this number could improve performance,
    but it will take more memory.

    Parameters
    ----------
    orthanc
        Orthanc object.
    max_worker
        Number of maximum workers for the concurrent building tree.

    Returns
    -------
    List[Patient]
        List of patient tree representation.
    """
    event_loop = asyncio.get_event_loop()

    return event_loop.run_until_complete(_build_patient_forest(orthanc))


async def _build_patient_forest(orthanc: Orthanc) -> List[Patient]:
    patient_identifiers = orthanc.get_patients().json()

    return [await _build_patient(i, orthanc) for i in patient_identifiers]


async def _build_patient(patient_identifier: str, orthanc: Orthanc) -> Patient:
    study_information = orthanc.get_patient_study_information(patient_identifier).json()
    study_identifiers = [study['ID'] for study in study_information]

    patient = Patient(patient_identifier, orthanc)
    patient.studies = [await _build_study(i, orthanc) for i in study_identifiers]

    return patient


async def _build_study(study_identifier: str, orthanc: Orthanc) -> Study:
    series_information = orthanc.get_study_series_information(study_identifier).json()
    series_identifiers = [series['ID'] for series in series_information]

    study = Study(study_identifier, orthanc)
    study.series = [await _build_series(i, orthanc) for i in series_identifiers]

    return study


async def _build_series(series_identifier: str, orthanc: Orthanc) -> Series:
    instance_information = orthanc.get_series_instance_information(series_identifier).json()
    instance_identifiers = [instance['ID'] for instance in instance_information]

    series = Series(series_identifier, orthanc)
    series.instances = [Instance(i, orthanc) for i in instance_identifiers]

    return series
