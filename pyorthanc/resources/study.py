from datetime import datetime
from typing import Dict, List

from .resource import Resource
from .series import Series
from .. import util


class Study(Resource):
    """Represent a study that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    def get_main_information(self) -> Dict:
        """Get Study information

        Returns
        -------
        Dict
            Dictionary of study information
        """
        if self.lock:
            if self._information is None:
                # Setup self._information for the first time when study is lock
                self._information = self.client.get_studies_id(self.id_)

            return self._information

        return self.client.get_studies_id(self.id_)

    @property
    def referring_physician_name(self) -> str:
        """Get referring physician name

        Returns
        -------
        str
            Referring physician Name.
        """
        return self.get_main_information()['MainDicomTags']['ReferringPhysicianName']

    @property
    def date(self) -> datetime:
        """Get study date

        The date have precision to the second (if available).

        Returns
        -------
        datetime
            Study date
        """
        date_string = self.get_main_information()['MainDicomTags']['StudyDate']
        time_string = self.get_main_information()['MainDicomTags']['StudyTime']

        return util.make_datetime_from_dicom_date(date_string, time_string)

    @property
    def study_id(self) -> str:
        """Get Study ID

        Returns
        -------
        str
            Study ID
        """
        try:
            return self.get_main_information()['MainDicomTags']['StudyID']
        except KeyError:
            return ''

    @property
    def uid(self) -> str:
        """Get StudyInstanceUID

        Returns
        -------
        str
            StudyInstanceUID
        """
        return self.get_main_information()['MainDicomTags']['StudyInstanceUID']

    @property
    def patient_identifier(self) -> str:
        """Get the Orthanc identifier of the parent patient

        Returns
        -------
        str
            Parent patient's identifier.
        """
        return self.get_main_information()['ParentPatient']

    @property
    def patient_information(self) -> Dict:
        """Get patient information

        Returns
        -------
        Dict
            Patient general information.
        """
        return self.get_main_information()['PatientMainDicomTags']

    @property
    def series(self) -> List[Series]:
        """Get Study series

        Returns
        -------
        List[Series]
            List of study's Series
        """
        if self.lock:
            if self._child_resources is None:
                series_information = self.client.get_studies_id_series(self.id_)
                self._child_resources = [Series(i['ID'], self.client, self.lock) for i in series_information]

            return self._child_resources

        series_information = self.client.get_studies_id_series(self.id_)

        return [Series(i['ID'], self.client, self.lock) for i in series_information]

    @property
    def is_stable(self):
        return self.get_main_information()['IsStable']

    @property
    def last_update(self) -> datetime:
        last_updated_date_and_time = self.get_main_information()['LastUpdate'].split('T')
        date = last_updated_date_and_time[0]
        time = last_updated_date_and_time[1]

        return util.make_datetime_from_dicom_date(date, time)

    @property
    def labels(self) -> List[str]:
        return self.get_main_information()['Labels']

    def add_label(self, label: str) -> None:
        self.client.put_studies_id_labels_label(self.id_, label)

    def remove_label(self, label):
        self.client.delete_studies_id_labels_label(self.id_, label)

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None, force: bool = False) -> 'Study':
        """Anonymize Study

        If no error has been raise, then it creates a new anonymous study.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            List of tag to keep unchanged
        force
            Some tags can't be change without forcing it (e.g. PatientID) for security reason

        Returns
        -------
        Study
            A new anonymous Study.
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        anonymous_study = self.client.post_studies_id_anonymize(
            self.id_,
            json={'Remove': remove, 'Replace': replace, 'Keep': keep, 'Force': force}
        )

        return Study(anonymous_study['ID'], self.client)

    def get_zip(self) -> bytes:
        """Get the bytes of the zip file

        Get the .zip file.

        Returns
        -------
        bytes
            Bytes of Zip file of the study.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Study
        a_study = Study(
            'STUDY_IDENTIFIER',
            Orthanc('http://localhost:8042')
        )
        bytes_content = a_study.get_zip()
        with open('study_zip_file_path.zip', 'wb') as file_handler:
            file_handler.write(bytes_content)
        ```

        """
        return self.client.get_studies_id_archive(self.id_)

    def remove_empty_series(self) -> None:
        """Delete empty series."""
        if self._child_resources is None:
            return

        for series in self._child_resources:
            series.remove_empty_instances()

        self._child_resources = [series for series in self._child_resources if series._child_resources != []]

    def __repr__(self):
        return f'Study(StudyId={self.study_id}, identifier={self.id_})'
