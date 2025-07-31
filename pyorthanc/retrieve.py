import os
from typing import List, Union

from ._resources.instance import Instance
from ._resources.patient import Patient
from ._resources.series import Series
from ._resources.study import Study


def retrieve_and_write_patients(patients: List[Patient], path: Union[str, os.PathLike]) -> None:
    """Retrieve and write patients to given path

    Parameters
    ----------
    patients
        List of patients.
    path
        Path where you want to write the files.
    """
    for patient in patients:
        retrieve_and_write_patient(patient, path)


def retrieve_and_write_patient(patient: Patient, path: Union[str, os.PathLike]) -> None:
    patient_id = patient.patient_id
    if patient_id == '':
        patient_path = os.path.join(path, 'unknown-patient')
    else:
        patient_path = os.path.join(path, patient.patient_id)

    for study in patient.studies:
        retrieve_and_write_study(study, patient_path)


def retrieve_and_write_study(study: Study, patient_path: Union[str, os.PathLike]) -> None:
    study_path = os.path.join(patient_path, study.uid)

    for series in study.series:
        retrieve_and_write_series(series, study_path)


def retrieve_and_write_series(series: Series, study_path: Union[str, os.PathLike]) -> None:
    series_path = os.path.join(study_path, series.uid)
    os.makedirs(series_path, exist_ok=True)

    for instance in series.instances:
        retrieve_and_write_instance(instance, series_path)


def retrieve_and_write_instance(instance: Instance, series_path) -> None:
    path = os.path.join(series_path, instance.uid + '.dcm')

    dicom_file_bytes = instance.get_dicom_file_content()

    with open(path, 'wb') as file_handler:
        file_handler.write(dicom_file_bytes)
