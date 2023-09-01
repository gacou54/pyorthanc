from datetime import datetime
from typing import Any, Dict, List

import pydicom

from .resource import Resource
from .. import util


class Instance(Resource):
    """Represent an instance that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Instance
    """

    def get_dicom_file_content(self) -> bytes:
        """Retrieves DICOM file

        This method retrieves bytes corresponding to DICOM file.

        Returns
        -------
        bytes
            Bytes corresponding to DICOM file

        Examples
        --------
        ```python
        from pyorthanc import Instance
        instance = Instance('instance_identifier',
                            Orthanc('http://localhost:8042'))
        dicom_file_bytes = instance.get_dicom_file_content()
        with open('your_path', 'wb') as file_handler:
            file_handler.write(dicom_file_bytes)
        ```
        """
        return self.client.get_instances_id_file(self.id_)

    @property
    def uid(self) -> str:
        """Get SOPInstanceUID"""
        return self._get_main_dicom_tag_value('SOPInstanceUID')

    def get_main_information(self) -> Dict:
        """Get instance information

        Returns
        -------
        Dict
            Dictionary with tags as key and information as value
        """
        if self.lock:
            if self._information is None:
                # Setup self._information for the first time when study is lock
                self._information = self.client.get_instances_id(self.id_)

            return self._information

        return self.client.get_instances_id(self.id_)

    @property
    def file_size(self) -> int:
        """Get the file size

        The output is in bytes. Divide by 1_000_000 to
        get it in Mb.

        Returns
        -------
        int
            The file size in bytes.
        """
        return self.get_main_information()['FileSize']

    @property
    def creation_date(self) -> datetime:
        """Get creation date

        The date have precision to the second.

        Returns
        -------
        datetime
            Creation Date
        """
        date_string = self.get_main_information()['MainDicomTags']['InstanceCreationDate']
        time_string = self.get_main_information()['MainDicomTags']['InstanceCreationTime']

        return util.make_datetime_from_dicom_date(date_string, time_string)

    @property
    def series_identifier(self) -> str:
        """Get the parent series identifier"""
        return self.get_main_information()['ParentSeries']
    
    @property
    def acquisition_number(self) -> int:
        return int(self._get_main_dicom_tag_value('AcquisitionNumber'))
    
    @property
    def image_index(self) -> int:
        return int(self._get_main_dicom_tag_value('ImageIndex'))

    @property
    def image_orientation_patient(self) -> List[float]:
        orientation = self._get_main_dicom_tag_value('ImageOrientationPatient')

        return [float(i) for i in orientation.split('\\')]

    @property
    def image_position_patient(self) -> List[float]:
        position = self._get_main_dicom_tag_value('ImagePositionPatient')

        return [float(i) for i in position.split('\\')]

    @property
    def image_comments(self) -> str:
        return self._get_main_dicom_tag_value('ImageComments')
    
    @property
    def instance_number(self) -> int:
        return int(self._get_main_dicom_tag_value('InstanceNumber'))
    
    @property
    def number_of_frames(self) -> int:
        return int(self._get_main_dicom_tag_value('NumberOfFrames'))

    @property
    def temporal_position_identifier(self) -> str:
        return self._get_main_dicom_tag_value('TemporalPositionIdentifier')

    @property
    def first_level_tags(self) -> Any:
        """Get first level tags"""
        return self.client.get_instances_id_content_tags_path(self.id_, '')

    @property
    def tags(self) -> Dict:
        """Get tags"""
        return dict(self.client.get_instances_id_tags(self.id_))

    @property
    def simplified_tags(self) -> Dict:
        """Get simplified tags"""
        return dict(self.client.get_instances_id_tags(self.id_, params={'simplify': True}))

    @property
    def labels(self) -> List[str]:
        """Get instance labels"""
        return self.get_main_information()['Labels']

    def add_label(self, label: str) -> None:
        """Add label to resource"""
        self.client.put_instances_id_labels_label(self.id_, label)

    def remove_label(self, label):
        """Remove label from resource"""
        self.client.delete_instances_id_labels_label(self.id_, label)

    def get_content_by_tag(self, tag: str) -> Any:
        """Get content by tag

        Parameters
        ----------
        tag
            Tag like 'ManufacturerModelName' or '0008-1090' or a group element like '' or '0008-1110/0/0008-1150'.

        Returns
        -------
        Any
            Content corresponding to specified tag.
        """
        result = self.client.get_instances_id_content_tags_path(id_=self.id_, tags_path=tag)

        try:
            return result.decode('utf-8').strip().replace('\x00', '')
        except AttributeError:
            return result

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None,
                  keep_private_tags: bool = False, keep_source: bool = True,
                  force: bool = False, dicom_version: str = None) -> bytes:
        """Anonymize Instance

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
        keep_private_tags
            If True, keep the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        bytes
            Raw bytes of the anonymized instance.
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        data = {
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'KeepPrivateTags': keep_private_tags,
            'KeepSource': keep_source,
        }

        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        return self.client.post_instances_id_anonymize(self.id_, data)

    def get_pydicom(self) -> pydicom.FileDataset:
        """Retrieve a pydicom.FileDataset object corresponding to the instance."""
        return util.get_pydicom(self.client, self.id_)
