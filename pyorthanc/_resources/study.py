from __future__ import annotations

from datetime import datetime
from typing import BinaryIO, Dict, List, TYPE_CHECKING, Union

from httpx import ReadTimeout

from .resource import Resource
from .series import Series
from .. import errors, util
from ..jobs import Job

if TYPE_CHECKING:
    from . import Patient


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
        return self.client.get_studies_id(self.id_)

    @property
    def legacy_viewer_url(self) -> str:
        """Get Study (legacy viewer) URL

        Returns
        -------
        str
            URL of study (legacy viewer)
        """
        return f'{self.client.url}/app/explorer.html#study?uuid={self.id_}'

    @property
    def referring_physician_name(self) -> str:
        """Get referring physician name"""
        return self._get_main_dicom_tag_value('ReferringPhysicianName')

    @property
    def requesting_physician(self) -> str:
        """Get referring physician name"""
        return self._get_main_dicom_tag_value('RequestingPhysician')

    @property
    def date(self) -> datetime:
        """Get study date

        The date have precision to the second (if available).

        Returns
        -------
        datetime
            Study date
        """
        date_string = self._get_main_dicom_tag_value('StudyDate')
        try:
            time_string = self._get_main_dicom_tag_value('StudyTime')
        except errors.TagDoesNotExistError:
            time_string = None

        return util.make_datetime_from_dicom_date(date_string, time_string)

    @property
    def study_id(self) -> str:
        """Get Study ID"""
        return self._get_main_dicom_tag_value('StudyID')

    @property
    def uid(self) -> str:
        """Get StudyInstanceUID"""
        return self._get_main_dicom_tag_value('StudyInstanceUID')

    @property
    def patient_identifier(self) -> str:
        """Get the Orthanc identifier of the parent patient"""
        return self.get_main_information()['ParentPatient']

    @property
    def parent_patient(self) -> Patient:
        from . import Patient
        return Patient(self.patient_identifier, self.client)

    @property
    def patient_information(self) -> Dict:
        """Get patient information"""
        return self.get_main_information()['PatientMainDicomTags']

    @property
    def series(self) -> List[Series]:
        """Get Study series"""
        if self._lock_children:
            if self._child_resources is None:
                series_ids = self.get_main_information()['Series']
                self._child_resources = [Series(i, self.client, self._lock_children) for i in series_ids]

            return self._child_resources

        series_ids = self.get_main_information()['Series']

        return [Series(i, self.client) for i in series_ids]

    @property
    def accession_number(self) -> str:
        return self._get_main_dicom_tag_value('AccessionNumber')

    @property
    def description(self) -> str:
        return self._get_main_dicom_tag_value('StudyDescription')

    @property
    def institution_name(self) -> str:
        return self._get_main_dicom_tag_value('InstitutionName')

    @property
    def requested_procedure_description(self) -> str:
        return self._get_main_dicom_tag_value('RequestedProcedureDescription')

    @property
    def is_stable(self) -> bool:
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

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None,
                  force: bool = False, keep_private_tags: bool = False,
                  keep_source: bool = True, priority: int = 0, permissive: bool = False,
                  private_creator: str = None, dicom_version: str = None) -> 'Study':
        """Anonymize study

        If no error has been raise, return an anonymous study.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method might be long to run, especially on large study or when multiple
        studies are anonymized. In those cases, it is recommended to use the `.anonymize_as_job()`

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            List of tag to keep unchanged
        force
            Some tags can't be changed without forcing it (e.g. StudyID) for security reason
        keep_private_tags
            If True, keep the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        priority
            Priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        private_creator
            The private creator to be used for private tags in replace.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Study
            A New anonymous study.

        Examples
        --------
        ```python
        new_study = study.anonymize()

        new_study_with_specific_study_id = study.anonymize(
            replace={'StudyDescription': 'A description'}
        )
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        data = {
            'Asynchronous': False,
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'KeepPrivateTags': keep_private_tags,
            'KeepSource': keep_source,
            'Priority': priority,
            'Permissive': permissive,
        }
        if private_creator is not None:
            data['PrivateCreator'] = private_creator
        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        try:
            anonymous_study = self.client.post_studies_id_anonymize(self.id_, data)
        except ReadTimeout:
            raise ReadTimeout(
                'Study anonymization is too long to process. '
                'Use `.anonymize_as_job` or increase client.timeout.'
            )

        return Study(anonymous_study['ID'], self.client)

    def anonymize_as_job(self, remove: List = None, replace: Dict = None, keep: List = None,
                         force: bool = False, keep_private_tags: bool = False,
                         keep_source: bool = True, priority: int = 0, permissive: bool = False,
                         private_creator: str = None, dicom_version: str = None) -> Job:
        """Anonymize study and return a job

        Launch an anonymization job.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method is useful when anonymizing large study or launching many
        anonymization jobs. The jobs are sent to Orthanc and processed according
        to the priority.

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            List of tag to keep unchanged
        force
            Some tags can't be changed without forcing it (e.g. StudyInstanceUID) for security reason
        keep_private_tags
            If True, keep the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        priority
            Priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        private_creator
            The private creator to be used for private tags in replace.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Job
            Return a Job object of the anonymization job.

        Examples
        --------
        For large study (recommended)
        ```python
        job = study.anonymize_as_job()
        job.state  # You can follow the job state

        job.wait_until_completion() # Or just wait on its completion
        new_study = Study(job.content['ID'], orthanc)
        ```
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        data = {
            'Asynchronous': True,
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'KeepPrivateTags': keep_private_tags,
            'KeepSource': keep_source,
            'Priority': priority,
            'Permissive': permissive,
        }
        if private_creator is not None:
            data['PrivateCreator'] = private_creator
        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        job_info = self.client.post_studies_id_anonymize(self.id_, data)

        return Job(job_info['ID'], self.client)

    def modify(self, remove: List = None, replace: Dict = None, keep: List = None,
               force: bool = False, remove_private_tags: bool = False,
               keep_source: bool = True, priority: int = 0, permissive: bool = False,
               private_creator: str = None) -> 'Study':
        """Modify study

        If no error has been raise, then create a modified version of the study.
        If keep=['StudyInstanceUID'] and force=True are use, then the study itself is changed.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method might be long to run, especially on large study or when multiple
        studies are modified. In those cases, it is recommended to use the `.modify_as_job()`

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
            Some tags can't be changed without forcing it (e.g. StudyInstanceUID) for security reason
        remove_private_tags
            If True, remove the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        priority
            Priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        private_creator
            The private creator to be used for private tags in Replace.

        Returns
        -------
        Study
            Returns a new modified study or returns itself if keep=['StudyInstanceUID']
            (in this case, the study itself is modified).

        Examples
        --------
        ```python
        # Create a modified study
        modified_study = study.modify(replace={'StudyInstanceUID': '1.2.840.113745.101000.1008000.38048.4626.5933732'}, force=True)
        assert modified_study.uid == '1.2.840.113745.101000.1008000.38048.4626.5933732'

        # Modify itself
        study.modify(replace={'ReferringPhysicianName': 'last^first'}, keep=['StudyInstanceUID'], force=True)
        assert study.referring_physician_name == 'last^first'
        ```
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        if 'StudyInstanceUID' in replace and not force:
            raise errors.ModificationError('If StudyInstanceUID is replaced, `force` must be `True`')

        data = {
            'Asynchronous': False,
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'RemovePrivateTags': remove_private_tags,
            'KeepSource': keep_source,
            'Priority': priority,
            'Permissive': permissive,
        }
        if private_creator is not None:
            data['PrivateCreator'] = private_creator

        try:
            modified_study = self.client.post_studies_id_modify(self.id_, data)
        except ReadTimeout:
            raise ReadTimeout(
                'Study modification is too long to process. '
                'Use `.modify_as_job` or increase client.timeout.'
            )

        # Reset cache since a main DICOM tag may have be changed
        self._main_dicom_tags = None

        # if 'StudyInstanceUID' is not affected, the modified_study['ID'] is the same as self.id_
        return Study(modified_study['ID'], self.client)

    def modify_as_job(self, remove: List = None, replace: Dict = None, keep: List = None,
                      force: bool = False, remove_private_tags: bool = False,
                      keep_source: bool = True, priority: int = 0, permissive: bool = False,
                      private_creator: str = None) -> Job:
        """Modify study and return a job

        Launch a modification job. If keep=['StudyInstanceUID'] (with `force=True`),
        then modified this study. If the StudyInstanceUID is not keeped, this creates
        a new modified study.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method is useful when modifying large study or launching many
        modification jobs. The jobs are sent to Orthanc and processed according
        to the priority.

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
            Allow the modification of tags related to DICOM identifiers, at the risk of breaking
            the DICOM model of the real world.
        remove_private_tags
            If True, remove the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        priority
            Priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        private_creator
            The private creator to be used for private tags in Replace.

        Returns
        -------
        Job
            Return a Job object of the modification job.

        Examples
        --------
        For large study (recommended)
        ```python
        job = study.modify_as_job(replace={'StudyDescription': 'a description'})
        job.state  # You can follow the job state

        job.wait_until_completion() # Or just wait on its completion
        modified_study = Study(job.content['ID'], client)
        assert modified_study.description == 'a description'
        ```
        Or modify the StudyInstanceUID
        ```python
        job = study.modify_as_job(
            replace={'StudyInstanceUID': '1.2.840.113745.101000.1008000.38048.4626.5933732'},
            force=True
        )
        job.wait_until_completion() # Or just wait on its completion

        modified_study = Study(job.content['ID'], client)
        modified_study.uid == '1.2.840.113745.101000.1008000.38048.4626.5933732'
        ```
        Or keep the StudyInstanceUID
        ```python
        job = study.modify_as_job(
            replace={'StudyDescription': 'a description'},
            keep=['StudyInstanceUID'],
            force=True
        )
        job.wait_until_completion()

        assert study.description == 'a description'
        ```
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        if 'StudyInstanceUID' in replace and not force:
            raise errors.ModificationError('If StudyInstanceUID is affected, `force` must be `True`')

        data = {
            'Asynchronous': True,
            'Remove': remove,
            'Replace': replace,
            'Keep': keep,
            'Force': force,
            'RemovePrivateTags': remove_private_tags,
            'KeepSource': keep_source,
            'Priority': priority,
            'Permissive': permissive,
        }
        if private_creator is not None:
            data['PrivateCreator'] = private_creator

        job_info = self.client.post_studies_id_modify(self.id_, data)

        # Reset cache since a main DICOM tag may have be changed
        self._main_dicom_tags = None

        return Job(job_info['ID'], self.client)

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
        a_study = Study('STUDY_IDENTIFIER', Orthanc('http://localhost:8042'))

        bytes_content = a_study.get_zip()
        with open('study_zip_file_path.zip', 'wb') as file_handler:
            file_handler.write(bytes_content)
        ```
        """
        return self.client.get_studies_id_archive(self.id_)

    def download(self, filepath: Union[str, BinaryIO], with_progres: bool = False) -> None:
        """Download the zip file to a target path or buffer

        This method is an alternative to the `.get_zip()` method for large files.
        The `.get_zip()` method will pull all the data in a single GET call,
        while `.download()` stream the data to a file or a buffer.
        Favor the `.download()` method to avoid timeout and memory issues.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Study
        a_study = Study('STUDY_IDENTIFIER', Orthanc('http://localhost:8042'))

        # Download a zip
        a_study.download('study.zip')

        # Download a zip and show progress
        a_study.download('study.zip', with_progres=True)

        # Or download in a buffer in memory
        buffer = io.BytesIO()
        a_study.download(buffer)
        # Now do whatever you want to do
        buffer.seek(0)
        zip_bytes = buffer.read()
        ```
        """
        self._download_file(f'{self.client.url}/studies/{self.id_}/archive', filepath, with_progres)

    def get_shared_tags(self, simplify: bool = False, short: bool = False) -> Dict:
        """Retrieve the shared tags of the study"""
        params = self._make_response_format_params(simplify, short)

        return dict(self.client.get_studies_id_shared_tags(
            self.id_,
            params=params
        ))

    @property
    def shared_tags(self) -> Dict:
        return self.get_shared_tags(simplify=True)

    def remove_empty_series(self) -> None:
        """Delete empty series."""
        if self._child_resources is None:
            return

        for series in self._child_resources:
            series.remove_empty_instances()

        self._child_resources = [series for series in self._child_resources if series._child_resources != []]
