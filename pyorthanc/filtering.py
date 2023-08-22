import asyncio
import warnings
from typing import Callable, Dict, List, Optional, Union

from .async_client import AsyncOrthanc
from .client import Orthanc
from .instance import Instance
from .patient import Patient
from .series import Series
from .study import Study
from .util import async_to_sync


def build_patient_forest(
        orthanc: Orthanc,
        patient_filter: Optional[Callable] = None,
        study_filter: Optional[Callable] = None,
        series_filter: Optional[Callable] = None) -> List[Patient]:
    warnings.warn(
        'Function "build_patient_forest" is deprecated and will be removed in a future release. '
        'Please use "find" instead',
        DeprecationWarning,
        stacklevel=2
    )
    return find(orthanc, patient_filter, study_filter, series_filter)


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
        Orthanc and AsyncOrthanc object.
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
        List of patient.
    """
    if isinstance(orthanc, AsyncOrthanc):
        patients = asyncio.run(
            _async_find(
                orthanc,
                patient_filter,
                study_filter,
                series_filter,
                instance_filter
            )
        )

        return trim_patient(patients)

    patient_identifiers = orthanc.get_patients()
    patients = []

    for patient_id in patient_identifiers:  # This ID is the Orthanc's ID, and not the PatientID
        patients.append(_build_patient(
            patient_id,
            orthanc,
            patient_filter,
            study_filter,
            series_filter,
            instance_filter
        ))

    return trim_patient(patients)


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

    return trim_patient(patients)


def _build_patient(
        patient_identifier: str,
        orthanc: Orthanc,
        patient_filter: Optional[Callable],
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Patient:
    patient = Patient(patient_identifier, orthanc)

    if patient_filter is not None:
        if not patient_filter(patient):
            return patient

    study_information = orthanc.get_patients_id_studies(patient_identifier)
    patient._studies = [_build_study(i, orthanc, study_filter, series_filter, instance_filter) for i in
                        study_information]

    return patient


async def _async_build_patient(
        patient_identifier: str,
        async_orthanc: AsyncOrthanc,
        patient_filter: Optional[Callable],
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Patient:
    patient = Patient(patient_identifier, async_to_sync(async_orthanc))

    if patient_filter is not None:
        if not patient_filter(patient):
            return patient

    study_information = await async_orthanc.get_patients_id_studies(patient_identifier)

    tasks = []
    for info in study_information:
        task = asyncio.create_task(
            _async_build_study(info, async_orthanc, study_filter, series_filter, instance_filter))
        tasks.append(task)

    patient._studies = await asyncio.gather(*tasks)

    return patient


def _build_study(
        study_information: Dict,
        orthanc: Orthanc,
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Study:
    study = Study(study_information['ID'], orthanc, study_information)

    if study_filter is not None:
        if not study_filter(study):
            return study

    series_information = orthanc.get_studies_id_series(study_information['ID'])
    study._series = [_build_series(i, orthanc, series_filter, instance_filter) for i in series_information]

    return study


async def _async_build_study(
        study_information: Dict,
        async_orthanc: AsyncOrthanc,
        study_filter: Optional[Callable],
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Study:
    study = Study(study_information['ID'], async_to_sync(async_orthanc), study_information)

    if study_filter is not None:
        if not study_filter(study):
            return study

    series_information = await async_orthanc.get_studies_id_series(study_information['ID'])

    tasks = []
    for info in series_information:
        task = asyncio.create_task(_async_build_series(info, async_orthanc, series_filter, instance_filter))
        tasks.append(task)

    study._series = await asyncio.gather(*tasks)

    return study


def _build_series(
        series_information: Dict,
        orthanc: Orthanc,
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Series:
    series = Series(series_information['ID'], orthanc, series_information)

    if series_filter is not None:
        if not series_filter(series):
            return series

    instance_information = orthanc.get_series_id_instances(series_information['ID'])
    series._instances = [_build_instance(i, orthanc, instance_filter) for i in instance_information]

    return series


async def _async_build_series(
        series_information: Dict,
        async_orthanc: AsyncOrthanc,
        series_filter: Optional[Callable],
        instance_filter: Optional[Callable]) -> Series:
    series = Series(series_information['ID'], async_to_sync(async_orthanc), series_information)

    if series_filter is not None:
        if not series_filter(series):
            return series

    instance_information = await async_orthanc.get_series_id_instances(series_information['ID'])
    series._instances = [_build_instance(i, async_to_sync(async_orthanc), instance_filter) for i in
                         instance_information]

    return series


def _build_instance(
        instance_information: Dict,
        orthanc: Orthanc,
        instance_filter: Optional[Callable]) -> Optional[Instance]:
    instance = Instance(instance_information['ID'], orthanc, instance_information)

    if instance_filter is not None:
        if not instance_filter(instance):
            return  # Means that the instance did not pass the filter criteria.

    return instance


def trim_patient(patients: List[Patient]) -> List[Patient]:
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
