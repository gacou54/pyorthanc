from datetime import datetime
from typing import Dict, Any

from pyorthanc.client import Orthanc


class Instance:
    """Represent an instance that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Instance
    """

    def __init__(
            self, instance_id: str,
            client: Orthanc,
            instance_information: Dict = None) -> None:
        """Constructor

        Parameters
        ----------
        instance_id
            Orthanc instance identifier.
        client
            Orthanc object.
        instance_information
            Dictionary of instance's information.
        """
        self.client = client

        self.id_ = instance_id
        self.information = instance_information

    def get_dicom_file_content(self) -> bytes:
        """Retrieves DICOM file

        This method retrieves bytes corresponding to DICOM file.

        Returns
        -------
        bytes
            Bytes corresponding to DICOM file

        Examples
        --------
        >>> from pyorthanc import Instance
        >>> instance = Instance('instance_identifier',
        ...                     Orthanc('http://localhost:8042'))
        >>> dicom_file_bytes = instance.get_dicom_file_content()
        >>> with open('your_path', 'wb') as file_handler:
        ...     file_handler.write(dicom_file_bytes)
        """
        return self.client.get_instances_id_file(self.id_)

    @property
    def identifier(self) -> str:
        """Get instance identifier

        Returns
        -------
        str
            Instance identifier
        """
        return self.id_

    @property
    def uid(self) -> str:
        """Get SOPInstanceUID

        Returns
        -------
        str
            SOPInstanceUID
        """
        return self.get_main_information()['MainDicomTags']['SOPInstanceUID']

    def get_main_information(self) -> Dict:
        """Get instance information

        Returns
        -------
        Dict
            Dictionary with tags as key and information as value
        """
        if self.information is None:
            self.information = self.client.get_instances_id(self.id_)

        return self.information

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

        return datetime(
            year=int(date_string[:4]),
            month=int(date_string[4:6]),
            day=int(date_string[6:8]),
            hour=int(time_string[:2]),
            minute=int(time_string[2:4]),
            second=int(time_string[4:6])
        )

    @property
    def series_id(self) -> str:
        """Get the parent series identifier

        Returns
        -------
        str
            The parent series identifier.
        """
        return self.get_main_information()['ParentSeries']

    @property
    def first_level_tags(self) -> Any:
        """Get first level tags

        Returns
        -------
        Any
            First level tags.
        """
        return self.client.get_instances_id_content_tags_path(self.id_, '')

    @property
    def tags(self) -> Dict:
        """Get tags

        Returns
        -------
        Dict
            Tags in the form of a dictionary.
        """
        return dict(self.client.get_instances_id_tags(self.id_))

    @property
    def simplified_tags(self) -> Dict:
        """Get simplified tags

        Returns
        -------
        Dict
            Simplified tags in the form of a dictionary.
        """
        return dict(self.client.get_instances_id_tags(self.id_, params={'simplify': True}))

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

    def __repr__(self):
        return f'Instance(identifier={self.id_})'
