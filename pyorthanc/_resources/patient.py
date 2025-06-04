import warnings
from datetime import datetime
from typing import BinaryIO, Dict, List, Union

from httpx import ReadTimeout

from .resource import Resource
from .study import Study
from .. import errors, util
from ..jobs import Job


class Patient(Resource):
    """Represent a Patient that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Patient
    """

    def get_main_information(self) -> Dict:
        """Get Patient information

        Returns
        -------
        Dict
            Dictionary of patient main information.
        """
        return self.client.get_patients_id(self.id_)

    @property
    def legacy_viewer_url(self) -> str:
        """Get Patient (legacy viewer) URL

        Returns
        -------
        str
            URL of patient (legacy viewer)
        """
        return f'{self.client.url}/app/explorer.html#patient?uuid={self.id_}'

    @property
    def patient_id(self) -> str:
        """Get patient ID"""
        return self._get_main_dicom_tag_value('PatientID')

    @property
    def name(self) -> str:
        """Get patient name"""
        return self._get_main_dicom_tag_value('PatientName')

    @property
    def birth_date(self) -> datetime:
        """Get patient birthdate"""
        date = self._get_main_dicom_tag_value('PatientBirthDate')

        return util.make_datetime_from_dicom_date(date)

    @property
    def sex(self) -> str:
        """Get patient sex"""
        return self._get_main_dicom_tag_value('PatientSex')

    @property
    def other_patient_ids(self) -> str:
        return self._get_main_dicom_tag_value('OtherPatientIDs').split('\\')

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
        self.client.put_patients_id_labels_label(self.id_, label)

    def remove_label(self, label):
        self.client.delete_patients_id_labels_label(self.id_, label)

    def get_zip(self) -> bytes:
        """Get the bytes of the zip file

        Get the .zip file.

        Returns
        -------
        bytes
            Bytes of Zip file of the patient.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Patient
        a_patient = Patient(
            'A_PATIENT_IDENTIFIER',
            Orthanc('http://localhost:8042')
        )
        bytes_content = a_patient.get_zip()
        with open('patient_zip_file_path.zip', 'wb') as file_handler:
            file_handler.write(bytes_content)
        ```
        """
        return self.client.get_patients_id_archive(self.id_)

    def download(self, filepath: Union[str, BinaryIO], with_progres: bool = False) -> None:
        """Download the zip file to a target path or buffer

        This method is an alternative to the `.get_zip()` method for large files.
        The `.get_zip()` method will pull all the data in a single GET call,
        while `.download()` stream the data to a file or a buffer.
        Favor the `.download()` method to avoid timeout and memory issues.

        Examples
        --------
        ```python
        from pyorthanc import Orthanc, Patient
        a_patient = Patient('A_PATIENT_IDENTIFIER', Orthanc('http://localhost:8042'))

        # Download a zip
        a_patient.download('patient.zip')

        # Download a zip and show progress
        a_patient.download('patient.zip', with_progres=True)

        # Or download in a buffer in memory
        buffer = io.BytesIO()
        a_patient.download(buffer)
        # Now do whatever you want to do
        buffer.seek(0)
        zip_bytes = buffer.read()
        ```
        """
        self._download_file(f'{self.client.url}/patients/{self.id_}/archive', filepath, with_progres)

    def get_patient_module(self, simplify: bool = False, short: bool = False) -> Dict:
        """Get patient module in a simplified version

        The method returns the DICOM patient module
        (PatientName, PatientID, PatientBirthDate, ...)

        Parameters
        ----------
        simplify
            Get the simplified version of the tags
        short
            Get the short version of the tags

        Returns
        -------
        Dict
            DICOM Patient module.
        """
        params = self._make_response_format_params(simplify, short)

        return dict(self.client.get_patients_id_module(
            self.id_,
            params=params
        ))

    @property
    def protected(self) -> bool:
        """Get if patient is protected against recycling

        Protection against recycling: False means unprotected, True protected.

        Returns
        -------
        bool
            False means unprotected, True means protected.
        """
        return '1' == self.client.get_patients_id_protected(self.id_)

    @protected.setter
    def protected(self, value: bool):
        # As of version 1.11.1, the Orthanc OPEN API file has missing information
        self.client._put(
            f'{self.client.url}/patients/{self.id_}/protected',
            json=1 if value else 0  # 1 means it will be protected, 0 means unprotected
        )

    def is_protected(self) -> bool:
        """Get if patient is protected against recycling

        Protection against recycling: False means unprotected, True protected.

        Returns
        -------
        bool
            False means unprotected, True means protected.
        """
        DeprecationWarning(
            '`patient.is_protected()` is deprecated and will be removed in future release. '
            'Use `patient.protected` instead.'
        )
        return self.protected

    def set_to_protected(self):
        """Set patient to protected state

        Returns
        -------
        None
            Nothing.
        """
        # As of version 1.11.1, the Orthanc OPEN API file has missing information
        warnings.warn(
            '`patient.set_to_protected()` is deprecated and will be removed in future release. '
            'Use `patient.protected = True` instead.',
            DeprecationWarning
        )
        self.protected = True

    def set_to_unprotected(self):
        """Set patient to unprotected state

        Returns
        -------
        None
            Nothing.
        """
        # As of version 1.11.1, the Orthanc OPEN API file has missing information
        warnings.warn(
            '`patient.set_to_protected()` is deprecated and will be removed in future release. '
            'Use `patient.protected = True` instead.',
            DeprecationWarning
        )
        self.protected = False

    @property
    def studies(self) -> List[Study]:
        """Get patient's studies

        Returns
        -------
        List[Study]
            List of the patient's studies
        """
        if self._lock_children:
            if self._child_resources is None:
                studies_ids = self.get_main_information()['Studies']
                self._child_resources = [Study(i, self.client, self._lock_children) for i in studies_ids]

            return self._child_resources

        studies_ids = self.get_main_information()['Studies']

        return [Study(i, self.client) for i in studies_ids]

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None,
                  force: bool = False, keep_private_tags: bool = False,
                  keep_source: bool = True, priority: int = 0, permissive: bool = False,
                  private_creator: str = None, dicom_version: str = None) -> 'Patient':
        """Anonymize patient

        If no error has been raise, then it creates a new anonymous patient.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method might be long to run, especially on large patient or when multiple
        patients are anonymized. In those cases, it is recommended to use the `.anonymize_as_job()`

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            List of tag to keep unchanged
        force
            Some tags can't be changed without forcing it (e.g. PatientID) for security reason
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
            The private creator to be used for private tags in Replace.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Patient
            A New anonymous patient.

        Examples
        --------
        ```python
        new_patient = patient.anonymize()

        new_patient_with_specific_patient_id = patient.anonymize(
            keep=['PatientName'],
            replace={'PatientID': 'TheNewPatientID'},
            force=True
        )
        ```
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
            anonymous_patient = self.client.post_patients_id_anonymize(self.id_, data)
        except ReadTimeout:
            raise ReadTimeout(
                'Patient anonymization is too long to process. '
                'Use `.anonymize_as_job` or increase client.timeout.'
            )

        return Patient(anonymous_patient['ID'], self.client)

    def anonymize_as_job(self, remove: List = None, replace: Dict = None, keep: List = None,
                         force: bool = False, keep_private_tags: bool = False,
                         keep_source: bool = True, priority: int = 0, permissive: bool = False,
                         private_creator: str = None, dicom_version: str = None) -> Job:
        """Anonymize patient and return a job

        Launch an anonymization job.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method is useful when anonymizing large patient or launching many
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
            Some tags can't be changed without forcing it (e.g. PatientID) for security reason
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
            The private creator to be used for private tags in Replace.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Job
            Return a Job object of the anonymization job.

        Examples
        --------
        For large patient (recommended)
        ```python
        job = patient.anonymize_as_job()
        job.state  # You can follow the job state

        job.wait_until_completion() # Or just wait on its completion
        new_patient = Patient(job.content['ID'], orthanc)
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

        job_info = self.client.post_patients_id_anonymize(self.id_, data)

        return Job(job_info['ID'], self.client)

    def modify(self, remove: List = None, replace: Dict = None, keep: List = None,
               force: bool = False, remove_private_tags: bool = False,
               keep_source: bool = True, priority: int = 0, permissive: bool = False,
               private_creator: str = None) -> 'Patient':
        """Modify patient

        If no error has been raise, then modify the patient. If the PatientID is replaced
        (with `force=True`), then return a new patient.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method might be long to run, especially on large patient or when multiple
        patients are modified. In those cases, it is recommended to use the `.modify_as_job()`

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
            Some tags can't be changed without forcing it (e.g. PatientID) for security reason
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
        Patient
            Returns a new patient if the "PatientID" tag has been replaced,
            returns itself if not (in this case, the patient itself is modified).

        Examples
        --------
        ```python
        patient.modify(remove=['PatientName'])
        patient.name  # will raise

        modified_patient = patient.modify(replace={'PatientID': 'TheNewPatientID'}, force=True)
        assert modified_patient.patient_id == 'TheNewPatientID'
        ```
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        if 'PatientID' in replace and not force:
            raise errors.ModificationError('If PatientID is replaced, `force` must be `True`')

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
            modified_patient = self.client.post_patients_id_modify(self.id_, data)
        except ReadTimeout:
            raise ReadTimeout(
                'Patient modification is too long to process. '
                'Use `.modify_as_job` or increase client.timeout.'
            )

        # Reset cache since a main DICOM tag may have be changed
        self._main_dicom_tags = None

        # if 'PatientID' is not affected, the modified_patient['ID'] is the same as self.id_
        return Patient(modified_patient['ID'], self.client)

    def modify_as_job(self, remove: List = None, replace: Dict = None, keep: List = None,
                      force: bool = False, remove_private_tags: bool = False,
                      keep_source: bool = True, priority: int = 0, permissive: bool = False,
                      private_creator: str = None) -> Job:
        """Modify patient and return a job

        Launch a modification job. If the PatientID is replaced (with `force=True`),
        then return a new patient. If the PatientID is not replaced, the patient itself is modified.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method is useful when modifying large patient or launching many
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
            Return a Job object of the anonymization job.

        Examples
        --------
        For large patient (recommended)
        ```python
        job = patient.modify_as_job(replace={'PatientName': 'NewName'})
        job.state  # You can follow the job state

        job.wait_until_completion() # Or just wait on its completion
        assert patient.name == 'NewName'
        ```
        Or modify the PatientID
        ```python
        job = patient.modify_as_job(replace={'PatientID': 'new-id'}, force=True)
        job.wait_until_completion() # Or just wait on its completion

        modified_patient = Patient(job.content['ID'], client)
        assert patient.patient_id != 'new_id'
        assert modified_patient.patient_id == 'new_id'
        ```
        """
        remove = [] if remove is None else remove
        replace = {} if replace is None else replace
        keep = [] if keep is None else keep

        if 'PatientID' in replace and not force:
            raise errors.ModificationError('If PatientID is affected, `force` must be `True`')

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

        job_info = self.client.post_patients_id_modify(self.id_, data)

        # Reset cache since a main DICOM tag may have be changed
        self._main_dicom_tags = None

        return Job(job_info['ID'], self.client)

    def get_shared_tags(self, simplify: bool = False, short: bool = False) -> Dict:
        """Retrieve the shared tags of the patient"""
        params = self._make_response_format_params(simplify, short)

        return dict(self.client.get_patients_id_shared_tags(
            self.id_,
            params=params
        ))

    @property
    def shared_tags(self) -> Dict:
        return self.get_shared_tags(simplify=True)

    def remove_empty_studies(self) -> None:
        """Delete empty studies."""
        if self._child_resources is None:
            return

        for study in self._child_resources:
            study.remove_empty_series()

        self._child_resources = [study for study in self._child_resources if study._child_resources != []]
