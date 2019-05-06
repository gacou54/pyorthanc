# coding: utf-8
# author: gabriel couture
from typing import List

from pyorthanc.datastructure.tree.patient import Patient
from pyorthanc.orthanc import Orthanc


def build_patient_forest(orthanc: Orthanc) -> List[Patient]:
    """Build a patient forest

    Each tree in the forest correspond to a patient. The layer in the
    tree correspond to:
        Patient -> Studies -> Series -> Instance

    Parameters
    ----------
    orthanc : Orthanc
        Orthanc object

    Returns
    -------
    List[Patient}
        List of patient tree representation
    """
    patient_identifiers: List[str] = orthanc.get_patients().json()

    return list(map(lambda i: Patient(i, orthanc), patient_identifiers))
