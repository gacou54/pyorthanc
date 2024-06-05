import asyncio
import warnings
from typing import Callable, Dict, List, Optional, Union

from . import util
from ._resources.instance import Instance
from ._resources.patient import Patient
from ._resources.series import Series
from ._resources.study import Study
from .async_client import AsyncOrthanc
from .client import Orthanc
from .util import async_to_sync


def find(orthanc: Union[Orthanc, AsyncOrthanc],
         patient_filter: Optional[Callable] = None,
         study_filter: Optional[Callable] = None,
         series_filter: Optional[Callable] = None,
         instance_filter: Optional[Callable] = None) -> List[Patient]:
    """Find desired patients/Study/Series/Instance in an Orthanc server

    This function builds a series of tree structure.
    Each tree correspond to a patient. The layers in the
    tree correspond to:

    `Patient -> Studies -> Series -> Instances`

    Parameters
    ----------
    orthanc
        Orthanc object.
    patient_filter
        Patient filter (e.g. lambda patient: patient.id_ == '03HDQ99*')
    study_filter
        Study filter (e.g. lambda study: study.study_id == '*pros*')
    series_filter
        Series filter (e.g. lambda series: series.modality == 'SR')
    instance_filter
        Instance filter (e.g. lambda instance: instance.SOPInstance == '...')

    Returns
    -------
    List[Patient]
        List of patients that respect .
    """
    # In this function, client that return raw responses are not supported.
    orthanc = util.ensure_non_raw_response(orthanc)

    if isinstance(orthanc, AsyncOrthanc):
        return asyncio.run(_async_find(
            async_orthanc=orthanc,
            patient_filter=patient_filter,
            study_filter=study_filter,
            series_filter=series_filter,
            instance_filter=instance_filter
        ))

    patients = [Patient(i, orthanc, _lock_children=True) for i in orthanc.get_patients()]
    if patient_filter is not None:
        patients = [i for i in patients if patient_filter(i)]

    for patient in patients:
        if study_filter is not None:
            patient._child_resources = [i for i in patient.studies if study_filter(i)]

        for study in patient.studies:
            if series_filter is not None:
                study._child_resources = [i for i in study.series if series_filter(i)]

            for series in study.series:
                if instance_filter is not None:
                    series._child_resources = [i for i in series.instances if instance_filter(i)]

    return trim_patients(patients)


async def _async_find(
        async_orthanc: AsyncOrthanc,
        patient_filter: Optional[Callable] = None,
        study_filter: Optional[Callable] = None,
        series_filter: Optional[Callable] = None,
        instance_filter: Optional[Callable] = None) -> List[Patient]:
    patient_identifiers = await async_orthanc.get_patients()
    tasks = []

    for patient_id in patient_identifiers:  # This ID is the Orthanc's ID, and not the PatientID
        task = asyncio.create_task(
            _async_build_patient(
                patient_id,
                async_orthanc,
                patient_filter,
                study_filter,
                series_filter,
                instance_filter
            )
        )
        tasks.append(task)

    patients = await asyncio.gather(*tasks)
    patients = list(patients)

    return trim_patients(patients)


async def _async_build_patient(
        patient_id_: str,
        async_orthanc: AsyncOrthanc,
        patient_filter: Optional[Callable],
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Patient:
    patient = Patient(patient_id_, async_to_sync(async_orthanc), _lock_children=True)

    if patient_filter is not None:
        if not patient_filter(patient):
            patient._child_resources = []
            return patient

    study_information = await async_orthanc.get_patients_id_studies(patient_id_)

    tasks = []
    for info in study_information:
        task = asyncio.create_task(
            _async_build_study(info, async_orthanc, study_filter, series_filter, instance_filter)
        )
        tasks.append(task)

    patient._child_resources = await asyncio.gather(*tasks)

    return patient


async def _async_build_study(
        study_information: Dict,
        async_orthanc: AsyncOrthanc,
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Study:
    study = Study(study_information['ID'], async_to_sync(async_orthanc), _lock_children=True)
    study._information = study_information

    if study_filter is not None:
        if not study_filter(study):
            study._child_resources = []
            return study

    series_information = await async_orthanc.get_studies_id_series(study_information['ID'])

    tasks = []
    for info in series_information:
        task = asyncio.create_task(_async_build_series(info, async_orthanc, series_filter, instance_filter))
        tasks.append(task)

    study._child_resources = await asyncio.gather(*tasks)

    return study


async def _async_build_series(
        series_information: Dict,
        async_orthanc: AsyncOrthanc,
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Series:
    series = Series(series_information['ID'], async_to_sync(async_orthanc), _lock_children=True)
    series._information = series_information

    if series_filter is not None:
        if not series_filter(series):
            series._child_resources = []
            return series

    instance_information = await async_orthanc.get_series_id_instances(series_information['ID'])
    series._child_resources = [
        _build_instance(i, async_to_sync(async_orthanc), instance_filter) for i in instance_information
    ]

    return series


def _build_instance(
        instance_information: Dict,
        orthanc: Orthanc,
        instance_filter: Optional[Callable]) -> Optional[Instance]:
    instance = Instance(instance_information['ID'], orthanc, _lock_children=True)
    instance._information = instance_information

    if instance_filter is not None:
        if not instance_filter(instance):
            return  # Means that the instance did not pass the filter criteria.

    return instance


def trim_patients(patients: List[Patient]) -> List[Patient]:
    """Trim Patient forest (list of patients)

    Parameters
    ----------
    patients
        Patient forest.

    Returns
    -------
    List[Patient]
        Pruned patient forest.
    """
    for patient in patients:
        patient.remove_empty_studies()

    patients = [p for p in patients if p.studies != []]

    return patients
