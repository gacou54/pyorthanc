import os
from typing import List

from .resources.instance import Instance
from .resources.patient import Patient
from .resources.series import Series
from .resources.study import Study


def retrieve_and_write_patients(patients: List[Patient], path: str) -> None:
    """Retrieve and write patients to given path

    Parameters
    ----------
    patients
        List of patients.
    path
        Path where you want to write the files.
    """
    os.makedirs(path, exist_ok=True)
    for patient in patients:
        retrieve_and_write_patient(patient, path)


def retrieve_and_write_patient(patient: Patient, path: str) -> None:
    patient_path = _make_patient_path(path, patient.patient_id)
    os.makedirs(patient_path, exist_ok=True)

    for study in patient.studies:
        retrieve_and_write_study(study, patient_path)


def retrieve_and_write_study(study: Study, patient_path: str) -> None:
    study_path = _make_study_path(patient_path, study.uid)
    os.makedirs(study_path, exist_ok=True)

    for series in study.series:
        retrieve_and_write_series(series, study_path)


def retrieve_and_write_series(series: Series, study_path: str) -> None:
    series_path = _make_series_path(study_path, series.modality)
    os.makedirs(series_path, exist_ok=True)

    for instance in series.instances:
        retrieve_and_write_instance(instance, series_path)


def retrieve_and_write_instance(instance: Instance, series_path) -> None:
    path = os.path.join(series_path, instance.uid + '.dcm')

    dicom_file_bytes = instance.get_dicom_file_content()

    with open(path, 'wb') as file_handler:
        file_handler.write(dicom_file_bytes)


def _make_patient_path(path: str, patient_id: str) -> str:
    patient_directories = os.listdir(path)

    if patient_id.strip() == '':
        patient_id = 'anonymous-patient'
        return os.path.join(path, _make_path_name(patient_id, patient_directories))

    return os.path.join(path, patient_id)


def _make_study_path(patient_path: str, study_uid: str) -> str:
    return os.path.join(patient_path, study_uid)


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
