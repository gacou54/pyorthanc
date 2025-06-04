from __future__ import annotations

from datetime import datetime
from typing import Any, BinaryIO, Dict, List, TYPE_CHECKING, Union

import pydicom

from .resource import Resource
from .. import errors, util

if TYPE_CHECKING:
    from . import Patient, Study, Series


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
        instance = Instance('instance_identifier', Orthanc('http://localhost:8042'))

        dicom_file_bytes = instance.get_dicom_file_content()
        with open('your_path', 'wb') as file_handler:
            file_handler.write(dicom_file_bytes)
        ```
        """
        return self.client.get_instances_id_file(self.id_)

    def download(self, filepath: Union[str, BinaryIO], with_progres: bool = False) -> None:
        """Download the DICOM file to a target path or buffer

        This method is an alternative to the `.get_dicom_file_content()` method for large files.
        The `.get_dicom_file_content()` method will pull all the data in a single GET call,
        while `.download()` stream the data to a file or a buffer.
        Favor the `.download()` method to avoid timeout and memory issues.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Instance
        instance = Instance('instance_identifier', Orthanc('http://localhost:8042'))

        # Download the dicom file
        instance.download('instance.dcm')

        # Download the file and show progress
        instance.download('instance.dcm', with_progres=True)

        # Or download in a buffer in memory
        buffer = io.BytesIO()
        instance.download(buffer)
        # Now do whatever you want to do
        buffer.seek(0)
        dicom_bytes = buffer.read()
        ```
        """
        self._download_file(f'{self.client.url}/instances/{self.id_}/file', filepath, with_progres)

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
        return self.client.get_instances_id(self.id_)

    @property
    def legacy_viewer_url(self) -> str:
        """Get Instance (legacy viewer) URL

        Returns
        -------
        str
            URL of instance (legacy viewer)
        """
        return f'{self.client.url}/app/explorer.html#instance?uuid={self.id_}'

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
        date_string = self._get_main_dicom_tag_value('InstanceCreationDate')
        time_string = self._get_main_dicom_tag_value('InstanceCreationTime')

        return util.make_datetime_from_dicom_date(date_string, time_string)

    @property
    def series_identifier(self) -> str:
        """Get the parent series identifier"""
        return self.get_main_information()['ParentSeries']

    @property
    def parent_series(self) -> Series:
        from . import Series
        return Series(self.series_identifier, self.client)

    @property
    def parent_study(self) -> Study:
        return self.parent_series.parent_study

    @property
    def parent_patient(self) -> Patient:
        return self.parent_study.parent_patient

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
        from warnings import warn
        warn("`Instance.first_level_tags` is deprecated. Use `Instance.tags` instead.")
        return self.tags

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
        result = self.client.get_instances_id_content_path(id_=self.id_, path=tag)

        try:
            return result.decode('utf-8').strip().replace('\x00', '')
        except AttributeError:
            return result

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None,
                  keep_private_tags: bool = False, keep_source: bool = True,
                  private_creator: str = None, force: bool = False, dicom_version: str = None) -> bytes:
        """Anonymize Instance

        If no error has been raise, then it creates a new anonymous instance.
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
            Some tags can't be changed without forcing it (e.g. SOPInstanceUID) for security reason
        keep_private_tags
            If True, keep the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        private_creator
            The private creator to be used for private tags in replace.
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
        if private_creator is not None:
            data['PrivateCreator'] = private_creator
        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        return self.client.post_instances_id_anonymize(self.id_, data)

    def modify(self, remove: List = None, replace: Dict = None, keep: List = None,
               remove_private_tags: bool = False, keep_source: bool = True,
               private_creator: str = None, force: bool = False) -> bytes:
        """Modify Instance

        If no error has been raise, then it creates a new modified instance.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            Keep the original value of the specified tags, to be chosen among the StudyInstanceUID,
            SeriesInstanceUID and SOPInstanceUID tags. Avoid this feature as much as possible,
            as this breaks the DICOM model of the real world.
        force
            Some tags can't be changed without forcing it (e.g. SOPInstanceUID) for security reason
        remove_private_tags
            If True, remove the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        private_creator
            The private creator to be used for private tags in replace.

        Returns
        -------
        bytes
            Raw bytes of the modified instance.
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        if 'SOPInstanceUID' in replace and not force:
            raise errors.ModificationError('If SOPInstanceUID is replaced, `force` must be `True`')

        data = {
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'RemovePrivateTags': remove_private_tags,
            'KeepSource': keep_source,
        }
        if private_creator is not None:
            data['PrivateCreator'] = private_creator

        return self.client.post_instances_id_modify(self.id_, data)

    def get_pydicom(self) -> pydicom.FileDataset:
        """Retrieve a pydicom.FileDataset object corresponding to the instance."""
        return util.get_pydicom(self.client, self.id_)
