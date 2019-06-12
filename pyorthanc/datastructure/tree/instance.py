# coding: utf-8
# author: gabriel couture
from typing import Dict, Any

from pyorthanc.orthanc import Orthanc


class Instance:
    """Represent an instance that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Instance
    """

    def __init__(
            self, instance_identifier: str,
            orthanc: Orthanc,
            instance_information: Dict = None) -> None:
        """Constructor

        Parameters
        ----------
        instance_identifier
            Orthanc instance identifier.
        orthanc
            Orthanc object.
        instance_information
            Dictionary of instance's information.
        """
        self.orthanc = orthanc

        self.instance_identifier = instance_identifier
        self.instance_information = instance_information

    def get_dicom_file_content(self) -> bytes:
        """Retrieves DICOM file

        This method retrieves bytes corresponding to DICOM file.

        Returns
        -------
        bytes
            Bytes corresponding to DICOM file

        Examples
        --------
        >>> instance = Instance('instance_identifier',
        ...                     Orthanc('http://localhost:8080'))
        >>> dicom_file_bytes = instance.get_dicom_file_content()
        >>> with open('your_path', 'wb') as file_handler:
        ...     file_handler.write(dicom_file_bytes)
        """
        return self.orthanc.get_instance_file(self.instance_identifier)

    def get_identifier(self) -> str:
        """Get instance identifier

        Returns
        -------
        str
            Instance identifier
        """
        return self.instance_identifier

    def get_main_information(self) -> Dict:
        """Get instance information

        Returns
        -------
        Dict
            Dictionary with tags as key and information as value
        """
        if self.instance_information is None:
            self.instance_information = self.orthanc.get_instance_information(
                self.instance_identifier)

        return self.instance_information

    def get_first_level_tags(self) -> Any:
        """Get first level tags

        Returns
        -------
        Any
            First level tags.
        """
        return self.orthanc.get_instance_first_level_tags(self.instance_identifier)

    def get_tags(self) -> Dict:
        """Get tags

        Returns
        -------
        Dict
            Tags in the form of a dictionary.
        """
        return self.orthanc.get_instance_tags(self.instance_identifier)

    def get_simplified_tags(self) -> Dict:
        """Get simplified tags

        Returns
        -------
        Dict
            Simplified tags in the form of a dictionary.
        """
        return self.orthanc.get_instance_simplified_tags(
            self.instance_identifier)

    def get_content_by_tag(self, tag: str) -> Any:
        """Get content by tag

        Parameters
        ----------
        tag
            Tag like '0040-a730'.

        Returns
        -------
        Any
            Content corresponding to specified tag.
        """
        return self.orthanc.get_instance_content_by_group_element(
            instance_identifier=self.instance_identifier,
            group_element=tag)

    def get_content_by_group_element(self, group_element: str) -> Any:
        """Get content by group element like '0040-a730/1/0040-a730'

        Parameters
        ----------
        group_element
            Group element like '0040-a730/1/0040-a730'.

        Returns
        -------
        Any
            Content corresponding to specified tag.
        """
        return self.orthanc.get_instance_content_by_group_element(
            instance_identifier=self.instance_identifier,
            group_element=group_element)

    def __str__(self):
        return f'Instance (identifier={self.get_identifier()})'
