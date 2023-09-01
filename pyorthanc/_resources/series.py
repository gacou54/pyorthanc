from datetime import datetime
from typing import Dict, List

from httpx import ReadTimeout

from .instance import Instance
from .resource import Resource
from .. import errors, util
from ..jobs import Job


class Series(Resource):
    """Represent a series that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Series
    """

    @property
    def instances(self) -> List[Instance]:
        """Get series instance"""
        if self.lock:
            if self._child_resources is None:
                instances_ids = self.get_main_information()['Instances']
                self._child_resources = [Instance(i, self.client, self.lock) for i in instances_ids]

            return self._child_resources

        instances_ids = self.get_main_information()['Instances']

        return [Instance(i, self.client, self.lock) for i in instances_ids]

    @property
    def uid(self) -> str:
        """Get SeriesInstanceUID"""
        return self._get_main_dicom_tag_value('SeriesInstanceUID')

    def get_main_information(self) -> Dict:
        """Get series main information"""
        if self.lock:
            if self._information is None:
                # Setup self._information for the first time when series is lock
                self._information = self.client.get_series_id(self.id_)

            return self._information

        return self.client.get_series_id(self.id_)

    @property
    def manufacturer(self) -> str:
        """Get the manufacturer"""
        return self._get_main_dicom_tag_value('Manufacturer')

    @property
    def study_identifier(self) -> str:
        """Get the parent study identifier"""
        return self.get_main_information()['ParentStudy']

    @property
    def date(self) -> datetime:
        """Get series datetime

        The date have precision to the second (if available).

        Returns
        -------
        datetime
            Series date
        """
        date_string = self._get_main_dicom_tag_value('SeriesDate')
        try:
            time_string = self._get_main_dicom_tag_value('SeriesTime')
        except errors.TagDoesNotExistError:
            time_string = None

        return util.make_datetime_from_dicom_date(date_string, time_string)

    @property
    def modality(self) -> str:
        """Get series modality"""
        return self._get_main_dicom_tag_value('Modality')

    @property
    def series_number(self) -> int:
        return int(self._get_main_dicom_tag_value('SeriesNumber'))

    @property
    def performed_procedure_step_description(self) -> str:
        return self._get_main_dicom_tag_value('PerformedProcedureStepDescription')

    @property
    def protocol_name(self) -> str:
        return self._get_main_dicom_tag_value('ProtocolName')

    @property
    def station_name(self) -> str:
        return self._get_main_dicom_tag_value('StationName')

    @property
    def description(self) -> str:
        return self._get_main_dicom_tag_value('StudyDescription')

    @property
    def body_part_examined(self) -> str:
        return self._get_main_dicom_tag_value('BodyPartExamined')
    
    @property
    def sequence_name(self) -> str:
        return self._get_main_dicom_tag_value('SequenceName')
    
    @property
    def cardiac_number_of_images(self) -> int:
        return int(self._get_main_dicom_tag_value('CardiacNumberOfImages'))

    @property
    def images_in_acquisition(self) -> int:
        return int(self._get_main_dicom_tag_value('ImagesInAcquisition'))
    
    @property
    def number_of_temporal_positions(self) -> int:
        return int(self._get_main_dicom_tag_value('NumberOfTemporalPositions'))

    @property
    def number_of_slices(self) -> int:
        return int(self._get_main_dicom_tag_value('NumberOfSlices'))

    @property
    def number_of_time_slices(self) -> int:
        return int(self._get_main_dicom_tag_value('NumberOfTimeSlices'))

    @property
    def image_orientation_patient(self) -> List[float]:
        orientation = self._get_main_dicom_tag_value('ImageOrientationPatient')

        return [float(i) for i in orientation.split('\\')]

    @property
    def series_type(self) -> str:
        return self._get_main_dicom_tag_value('SeriesType')
    
    @property
    def operators_name(self) -> str:
        return self._get_main_dicom_tag_value('OperatorsName')
    
    @property
    def acquisition_device_processing_description(self) -> str:
        return self._get_main_dicom_tag_value('AcquisitionDeviceProcessingDescription')
    
    @property
    def contrast_bolus_agent(self) -> str:
        return self._get_main_dicom_tag_value('ContrastBolusAgent')

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
        self.client.put_series_id_labels_label(self.id_, label)

    def remove_label(self, label):
        self.client.delete_series_id_labels_label(self.id_, label)

    def anonymize(self, remove: List = None, replace: Dict = None, keep: List = None,
                  force: bool = False, keep_private_tags: bool = False,
                  keep_source: bool = True, priority: int = 0, permissive: bool = False,
                  dicom_version: str = None) -> 'Series':
        """Anonymize series

        If no error has been raise, return an anonymous series.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method might be long to run, especially on large series or when multiple
        seriess are anonymized. In those cases, it is recommended to use the `.anonymize_as_job()`

        Parameters
        ----------
        remove
            List of tag to remove
        replace
            Dictionary of {tag: new_content}
        keep
            List of tag to keep unchanged
        force
            Some tags can't be changed without forcing it (e.g. SeriesID) for security reason
        keep_private_tags
            If True, keep the private tags from the DICOM instances.
        keep_source
            If False, instructs Orthanc to the remove original resources.
            By default, the original resources are kept in Orthanc.
        priority
            In asynchronous mode, the priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Series
            A New anonymous series.

        Examples
        --------
        ```python
        new_series = series.anonymize()

        new_series_with_specific_series_id = series.anonymize(
            replace={'SeriesDescription': 'A description'}
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
        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        try:
            anonymous_series = self.client.post_series_id_anonymize(self.id_, data)
        except ReadTimeout:
            raise ReadTimeout(
                'Series anonymization is too long to process. '
                'Use `.anonymize_as_job` or increase client.timeout.'
            )

        return Series(anonymous_series['ID'], self.client)

    def anonymize_as_job(self, remove: List = None, replace: Dict = None, keep: List = None,
                         force: bool = False, keep_private_tags: bool = False,
                         keep_source: bool = True, priority: int = 0, permissive: bool = False,
                         dicom_version: str = None) -> Job:
        """Anonymize series and return a job

        Launch an anonymization job.
        Documentation: https://book.orthanc-server.com/users/anonymization.html

        Notes
        -----
        This method is useful when anonymizing large series or launching many
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
            In asynchronous mode, the priority of the job. The lower the value, the higher the priority.
        permissive
            If True, ignore errors during the individual steps of the job.
        dicom_version
            Version of the DICOM standard to be used for anonymization.
            Check out configuration option DeidentifyLogsDicomVersion for possible values.

        Returns
        -------
        Job
            Return a Job object of the anonymization job.

        Examples
        --------
        For large series (recommended)
        ```python
        job = series.anonymize_as_job(asynchronous=True)
        job.state  # You can follow the job state

        job.wait_until_completion() # Or just wait on its completion
        new_series = Patient(job.content['ID'], orthanc)
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
        if dicom_version is not None:
            data['DicomVersion'] = dicom_version

        job_info = self.client.post_series_id_anonymize(self.id_, data)

        return Job(job_info['ID'], self.client)

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

    def remove_empty_instances(self) -> None:
        if self._child_resources is not None:
            self._child_resources = [i for i in self._child_resources if i is not None]
