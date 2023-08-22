from typing import List, Union, Iterable

from .client import Orthanc
from .patient import Patient
from .instance import Instance
from .series import Series
from .study import Study

LOOKUP_INTERVAL = 1_000


class Labels:
    """Utility class for finding resources that correspond to desired labels"""

    def __init__(self, client: Orthanc):
        self.client = client

    def __iter__(self):
        for label in self.client.get_tools_labels():
            yield label

    def __repr__(self) -> str:
        return str(self.client.get_tools_labels())

    def __len__(self) -> int:
        return len(self.client.get_tools_labels())

    def __contains__(self, item: str) -> bool:
        return item in self.client.get_tools_labels()

    def __eq__(self, other: Union[Iterable, 'Labels']) -> bool:
        if isinstance(other, Iterable):
            return sorted(self.client.get_tools_labels()) == sorted(other)

        return sorted(self.client.get_tools_labels()) == sorted(other.client.get_tools_labels())

    def find_patients(self, label: str) -> List[Patient]:
        since = 0
        patients = []

        while True:
            result = self.client.get_patients(params={
                'expand': True,
                'limit': LOOKUP_INTERVAL,
                'since': since
            })
            if len(result) == 0:
                break

            patients += [Patient(i['ID'], self.client, patient_information=i) for i in result if label in i['Labels']]
            since = LOOKUP_INTERVAL

        return patients

    def find_studies(self, label: str) -> List[Study]:
        result = self.client.get_studies(params={'expand': True})

        return [Study(i['ID'], self.client, study_information=i) for i in result if label in i['Labels']]

    def find_series(self, label: str) -> List[Series]:
        result = self.client.get_series(params={'expand': True})

        return [Series(i['ID'], self.client, series_information=i) for i in result if label in i['Labels']]

    def find_instances(self, label: str) -> List[Instance]:
        result = self.client.get_instances(params={'expand': True})

        return [Instance(i['ID'], self.client, instance_information=i) for i in result if label in i['Labels']]
