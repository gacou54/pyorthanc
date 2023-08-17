from datetime import datetime
from typing import Dict, List

from .instance import Instance
from .resource import Resource
from .. import util


class Series(Resource):
    """Represent a series that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    @property
    def instances(self) -> List[Instance]:
        """Get series instance

        Returns
        -------
        List[Instance]
            List of the series' Instance.
        """
        if self.lock:
            if self._child_resources is None:
                instances_information = self.client.get_series_id_instances(self.id_)
                self._child_resources = [Instance(i['ID'], self.client, self.lock) for i in instances_information]

            return self._child_resources

        instances_information = self.client.get_series_id_instances(self.id_)

        return [Instance(i['ID'], self.client, self.lock) for i in instances_information]

    @property
    def uid(self) -> str:
        """Get SeriesInstanceUID

        Returns
        -------
        str
            SeriesInstanceUID
        """
        return self.get_main_information()['MainDicomTags']['SeriesInstanceUID']

    def get_main_information(self) -> Dict:
        """Get series main information

        Returns
        -------
        Dict
            Dictionary of series main information.
        """
        if self.lock:
            if self._information is None:
                # Setup self._information for the first time when series is lock
                self._information = self.client.get_series_id(self.id_)

            return self._information

        return self.client.get_series_id(self.id_)

    @property
    def manufacturer(self) -> str:
        """Get the manufacturer

        Returns
        -------
        str
            The manufacturer.
        """
        return self.get_main_information()['MainDicomTags']['Manufacturer']

    @property
    def study_identifier(self) -> str:
        """Get the parent study identifier

        Returns
        -------
        str
            The parent study identifier.
        """
        return self.get_main_information()['ParentStudy']

    @property
    def modality(self) -> str:
        """Get series modality

        Returns
        -------
        str
            Series modality.
        """
        return self.get_main_information()['MainDicomTags']['Modality']

    @property
    def series_number(self) -> str:
        """Get series number

        Returns
        -------
        str
            Series number.
        """
        return self.get_main_information()['MainDicomTags']['SeriesNumber']

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
        self.client.put_series_id_labels_label(self.id_, label)

    def remove_label(self, label):
        self.client.delete_series_id_labels_label(self.id_, label)

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None, force: bool = False) -> 'Series':
        """Anonymize Series

        If no error has been raise, then it creates a new anonymous series.
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
        Series
            A new anonymous Series.
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        anonymous_series = self.client.post_series_id_anonymize(
            self.id_,
            json={'Remove': remove, 'Replace': replace, 'Keep': keep, 'Force': force}
        )

        return Series(anonymous_series['ID'], self.client)

    def get_zip(self) -> bytes:
        """Get the bytes of the zip file

        Get the .zip file.

        Returns
        -------
        bytes
            Bytes of Zip file of the series.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Series
        a_series = Series(
            'SERIES_IDENTIFIER',
            Orthanc('http://localhost:8042')
        )
        bytes_content = a_series.get_zip()
        with open('series_zip_file_path.zip', 'wb') as file_handler:
            file_handler.write(bytes_content)
        ```

        """
        return self.client.get_series_id_archive(self.id_)

    def __repr__(self):
        return f'Series(identifier={self.id_})'

    def remove_empty_instances(self) -> None:
        if self._child_resources is not None:
            self._child_resources = [i for i in self._child_resources if i is not None]
