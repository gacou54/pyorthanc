# coding: utf-8
from typing import List, Dict

import requests
from requests.auth import HTTPBasicAuth


class Orthanc:
    """Wrapper around Orthanc REST API

    You need to know if you need credentials before using this
    object. If yes, you need to set credentials with the method
    `setup_credential`.
    """

    def __init__(self, orthanc_url: str):
        """Constructor

        Parameters
        ----------
        orthanc_url : str
            Orthanc server address
        """
        self._orthanc_url: str = orthanc_url

        self._credentials_are_set: bool = False
        self._credentials: HTTPBasicAuth = None

    def setup_credentials(self, username: str, password: str) -> None:
        """Set credentials needed for HTTP requests

        Parameters
        ----------
        username : Username.
        password : Password.
        """
        self._credentials = HTTPBasicAuth(username, password)
        self._credentials_are_set = True

    def get_request(self, route: str, params: Dict = None,
                    **kwargs) -> requests.Response:
        """GET request with specified route

        Parameters
        ----------
        route : HTTP route.
        params : Params with the HTTP GET request.

        Returns
        -------
        requests.Response
            Response of the HTTP GET request.
        """
        if self._credentials_are_set:
            return requests.get(
                route, params=params, auth=self._credentials, **kwargs)

        return requests.get(route, params=params, **kwargs)

    def delete_request(self, route: str, **kwargs) -> requests.Response:
        """DELETE to specified route

        Parameters
        ----------
        route : HTTP route.

        Returns
        -------
        requests.Response
            Response of the HTTP DELETE request.
        """
        if self._credentials_are_set:
            return requests.delete(route, auth=self._credentials, **kwargs)

        return requests.delete(route, **kwargs)

    def post_request(self, route: str, data: Dict = None, json=None,
                     **kwargs) -> requests.Response:
        """POST to specified route

        Parameters
        ----------
        route : HTTP route.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Response of the HTTP POST request.
        """
        if self._credentials_are_set:
            return requests.post(
                route, auth=self._credentials, data=data, json=json, **kwargs)

        return requests.post(route, data=data, json=json, **kwargs)

    def put_request(self, route: str, data: Dict = None, json=None,
                    **kwargs) -> requests.Response:
        """PUT to specified route

        Parameters
        ----------
        route : str
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Response of the HTTP PUT requests
        """
        if self._credentials_are_set:
            return requests.put(
                route, auth=self._credentials, data=data, json=json, **kwargs)

        return requests.put(route, data, json=json, **kwargs)

    def get_attachments(
            self, resource_type: str,
            identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get list of files attached to the object identifier

        List the files that are attached to this patient, study, series or instance

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of files attached to the object corresponding to the object identifier
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments',
            params=params,
            **kwargs)

    def get_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment file corresponding to object identifier and attachment's name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment file corresponding to object identifier and attachment's name
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            params=params,
            **kwargs)

    def delete_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            **kwargs) -> requests.Response:
        """Delete attachment by name

        Delete the specified attachment file.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            **kwargs)

    def put_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put attachment with given name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : Data to send in the request's body.
        json : json to send in the request's body.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            data=data,
            json=json,
            **kwargs)

    def post_compress_attachment(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Compress attachment file

        This method should compress the DICOM instance(s).

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : Data to send in the request's body.
        json : json to send in the request's body.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compress',
            data=data,
            json=json,
            **kwargs)

    def get_attachment_compressed_data(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment compressed data

        Return the (possibly compressed) data, as stored on the disk.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            The (possibly compressed) data, as stored on the disk.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_data',
            params=params,
            **kwargs)

    def get_attachment_compressed_data_md5(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment by name as compressed data in md5

        Return the (possibly compressed) data, with md5 encryption.
        Note that md5 is not a safe encryption and should not be used if
        real encryption is needed.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            The (possibly compressed) data, with md5 encryption.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_md5',
            params=params,
            **kwargs)

    def get_attachment_compressed_size(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment compressed size

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment compressed size.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_size',
            params=params,
            **kwargs)

    def get_attachment_data(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment data

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment data.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/data',
            params=params,
            **kwargs)

    def is_attachment_compressed(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Ask Orthanc if attachment is compressed

        Is this attachment compressed: "0" means uncompressed, "1" compressed

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            "0" means uncompressed, "1" compressed
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/is_compressed',
            params=params,
            **kwargs)

    def get_attachment_md5(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment with md5 encoding

        Note that md5 is not a safe encryption and should not be used if
        real encryption is needed.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment with md5 encoding.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/md5',
            params=params,
            **kwargs)

    def get_attachment_size(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment size

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment size.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/size',
            params=params,
            **kwargs)

    def post_attachment_uncompress(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post an uncompressed attachment

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/uncompress',
            data=data,
            json=json,
            **kwargs)

    def post_attachment_verify_md5(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post that verify that there is no corruption on the disk

        Check that there is no corruption on the disk (HTTP status == 200 iff. no error)

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/verify_md5',
            data=data,
            json=json,
            **kwargs)

    def get_object_metadata(
            self, resource_type: str,
            identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get object's metadata with specified resource-type and identifier

        "?expand" argument

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Object Metadata.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata',
            params=params,
            **kwargs)

    def get_metadata_contents_of_specified_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get the contents of the specified metadata field/name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Contents of specified metadata field.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            params=params,
            **kwargs)

    def delete_metadata_contents_of_specified_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            **kwargs) -> requests.Response:
        """Delete the contents of the specified metadata field/name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            **kwargs)

    def put_metadata_contents_with_specific_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put the contents with a specified metadata field/name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : PUT HTTP request's data.
        json : PUT HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            data=data,
            json=json,
            **kwargs)

    def get_changes(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get changes (last, since or with specified limit)

        With "last", "limit" and "since" arguments.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Changes (depends on given params/arguments)
        """
        return self.get_request(f'{self._orthanc_url}/changes', params=params, **kwargs)

    def delete_changes(self, **kwargs) -> requests.Response:
        """Delete changes (last, since or with specified limit)

        With "last", "limit" and "since" arguments.

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/changes', **kwargs)

    def get_exports(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get exports

        With "last", "limit" and "since" arguments

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            The exports.
        """
        return self.get_request(f'{self._orthanc_url}/exports', params=params, **kwargs)

    def delete_exports(self, **kwargs) -> requests.Response:
        """Delete exports

        "last", "limit" and "since" arguments

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/exports', **kwargs)

    def get_instances(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get all instances identifiers

        Arguments : "last" and "limit"

        Parameters
        ----------
        params : GET HTTP request's params.

        -------
        requests.Response
            All instances identifiers.
        """
        return self.get_request(f'{self._orthanc_url}/instances', params=params, **kwargs)

    def post_instances(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post instances

        Add the new DICOM file given in the POST body.

        Parameters
        ----------
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(f'{self._orthanc_url}/instances', data=data, json=json, **kwargs)

    def get_instance(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance

        Instance dictionary with main information.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance dictionary with main information.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}', params=params, **kwargs)

    def delete_instance(self, instance_identifier: str, **kwargs) -> requests.Response:
        """Delete specified instance

        Parameters
        ----------
        instance_identifier : Instance identifier.

        Returns
        -------
        requests.Response
            HTTP Status == 200 if no error.
        """
        return self.delete_request(f'{self._orthanc_url}/instances/{instance_identifier}', **kwargs)

    def anonymize_specified_instance(
            self, instance_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Anonymize specified instance

        http://book.orthanc-server.com/users/anonymization.html

        Parameters
        ----------
        instance_identifier : Instance identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_instance_content(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance content (first level DICOM tags)

        List the first-level DICOM tags

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance's first level DICOM tags.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/content/',
            params=params,
            **kwargs)

    def get_instance_content_of_group_element(
            self, instance_identifier: str,
            group_element: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get value of DICOM tags corresponding to a specified group element

        Raw access to the value of DICOM tags (comprising the padding character).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        group_element : Group element corresponding to targeted DICOM tag.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            DICOM tag value.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/content/{group_element}',
            params=params,
            **kwargs)

    def get_instance_content_of_group_element_at_specified_indexes(
            self, instance_identifier: str,
            group_element: str,
            indexes: List[str],
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get value of DICOM tags corresponding to a specified group element at specified indexes

        Raw access to the content of DICOM sequences.

        Parameters
        ----------
        instance_identifier : instance identifier.
        group_element : Group element corresponding to targeted DICOM tag.
        indexes : Sequences on indexes to have access to.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Content of DICOM instances indexes sequences.
        """
        formatted_indexes = ''

        for index in indexes:
            formatted_indexes += index + '/'

        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/content/{group_element}/{formatted_indexes}',
            params=params,
            **kwargs)

    def export_instance_to_filesystem(
            self, instance_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Write the DICOM file to filesystem

        Write the DICOM file to the filesystem where Orthanc is running.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/export',
            data=data,
            json=json,
            **kwargs)

    def get_instance_file(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance DICOM file
        
        Retrieve on local computer the instance file in bytes.

        Parameters
        ----------
        identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Bytes corresponding to DICOM file.

        Examples
        --------
        >>> orthanc = Orthanc('ORTHANC_URL')
        >>> dicom_file_bytes = orthanc.get_instance_file('an_instance_identifier').json()
        >>> with open('your_path', 'wb') as file_handler:
        ...     file_handler.write(dicom_file_bytes)

        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/file',
            params=params,
            **kwargs)

    def get_instance_frames(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get Instances's frames

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Frames of specified instance.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames',
            params=params,
            **kwargs)

    def get_instance_frame_as_int16_image(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance frame as int16 image

        Truncated decoded image to the [-32768;32767] range
        (Accepts image/png, image/jpg, image/x-portable-arbitrarymap).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance frame as int16 image.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image_int16',
            params=params,
            **kwargs)

    def get_instance_frame_as_image_uint16(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance frame as uint16 image

        Truncated decoded image to the [0;65535] range
         (Accepts image/png, image/jpg, image/x-portable-arbitrarymap).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image_uint16',
            params=params,
            **kwargs)

    def get_instance_frame_as_image_uint8(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance frame as uint16 image

        Truncated decoded image to the [0;255] range
         (Accepts image/png, image/jpg, image/x-portable-arbitrarymap).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image_uint8',
            params=params,
            **kwargs)

    def get_instance_frame_as_readable_image_by_matlab(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance frame as a readable image by matlab

        Get a kind of array :
        a = eval(urlread('http://localhost:8042/instances/.../frames/0/matlab'))

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/matlab',
            params=params,
            **kwargs)

    def get_preview_of_instance_frame(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get a preview of an instance frame

        Rescaled image (so that all the range [0;255] is used)

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
           A rescaled image (so that all the range [0;255] is used) corresponding to specified frame.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/preview',
            params=params,
            **kwargs)

    def get_raw_content_of_instance_frame(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get raw content of an instance frame (bypass image decoding)

        Access to the raw content of one frame (bypass image decoding).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Raw content of one frame (bypass image decoding).
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/raw',
            params=params,
            **kwargs)

    def get_raw_compressed_content_of_instance_frame(
            self, instance_identifier: str,
            frame_number: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get raw content of an instance frame (compressed using gzip)

        Access to the raw content of one frame, compressed using gzip.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        frame_number : Frame number.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Raw content of one frame, compressed using gzip
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/raw.gz',
            params=params,
            **kwargs)

    def get_instance_header(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get the meta information (header) of the DICOM file

        Get the meta information (header) of the DICOM file,
         "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Meta information (header) of the DICOM file.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/header',
            params=params,
            **kwargs)

    def get_instance_image_as_int16(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance image as an int16 image

        Truncated decoded image to the [-32768;32767] range
         (Accepts image/png, image/jpg, image/x-portable-arbitrarymap).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance image as an int16 image.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/image_int16',
            params=params,
            **kwargs)

    def get_instance_image_as_uint16(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance image as an uint16 image

        Truncated decoded image to the [0;65535] range
         (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance image as an uint16 image.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/image_uint16',
            params=params,
            **kwargs)

    def get_instance_image_as_uint8(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance image as an uint8 image

        Truncated decoded image to the [0;255] range
         (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance image as an uint8 image.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/image_uint8',
            params=params,
            **kwargs)

    def get_instance_image_as_readable_image_by_matlab(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance image that is readable by matlab

        a = eval(urlread('http://localhost:8042/instances/.../matlab'))

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance image that is readable by matlab.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/matlab',
            params=params,
            **kwargs)

    def modify_instance(
            self, instance_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Modify instance

        See http://book.orthanc-server.com/users/anonymization.html .

        Parameters
        ----------
        instance_identifier : Instance identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_instance_module(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance module

        "?simplify" argument to simplify output, "?short"

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance module.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/module',
            params=params,
            **kwargs)

    def get_instance_patient_identifier(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's patient's identifier

        Retrieve the parent patient of this instance.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Patient identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/patient',
            params=params,
            **kwargs)

    def get_instance_pdf(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get the PDF inside the DICOM file, if any.

        Return the encapsulated PDF inside the DICOM file, if any.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            PDF inside the DICOM file, if any.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/pdf',
            params=params,
            **kwargs)

    def get_preview_of_instance_image(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get a preview of an instance image

        Rescaled image (so that all the range [0;255] is used).

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
           A rescaled image (so that all the range [0;255] is used).
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/preview',
            params=params,
            **kwargs)

    def reconstruct_main_dicom_tags_of_instance(
            self, instance_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Reconstruction of the main DICOM tags

        Force reconstruction of the main DICOM tags, JSON summary and metadata.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_instance_series_identifier(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's series's identifier

        Retrieve the parent series of this instance.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series's identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/series',
            params=params,
            **kwargs)

    def get_instance_simplified_tags(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's simplified DICOM tags

        Instance simplified DICOM tags (e.g. "PatientID" instead of "(0010,0020)").

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance's simplified DICOM tags. Should be in the form of a dictionary.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/simplified_tags',
            params=params,
            **kwargs)

    def get_instance_statistics(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's statistics

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance's statistics.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/statistics',
            params=params,
            **kwargs)

    def get_instance_study_identifier(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's study's identifier

        Retrieve the parent study of this instance.

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance's study's identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/study',
            params=params,
            **kwargs)

    def get_instance_tags(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance's tags.

        "?simplify" argument to simplify output (same as "simplified-tags"), "?short"

        Parameters
        ----------
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Instance's DICOM tags. Should be in the form of a dictionary.
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/tags',
            params=params,
            **kwargs)

    def get_jobs(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get running jobs

        List the jobs, "?expand" to get more information

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of running jobs identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs', params=params, **kwargs)

    def get_job_information(
            self, job_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get information of specified job

        Get information about specified job.

        Parameters
        ----------
        job_identifier : Job identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Information about specified job.
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs/{job_identifier}', params=params, **kwargs)

    def cancel_job(
            self, job_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Cancel specified job

        Cancel the job, tag it as failed

        Parameters
        ----------
        job_identifier : Job identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{job_identifier}/cancel',
            data=data,
            json=json,
            **kwargs)

    def pause_job(
            self, job_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Pause specified job

        Pause the specified job.

        Parameters
        ----------
        job_identifier : Job identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{job_identifier}/pause',
            data=data,
            json=json,
            **kwargs)

    def resubmit_job(
            self, job_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Resubmit job

        Resubmit a failed job.

        Parameters
        ----------
        job_identifier : Job identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{job_identifier}/resubmit',
            data=data,
            json=json,
            **kwargs)

    def resume_job(
            self, job_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Resume the specified paused job

        Resume a paused job.

        Parameters
        ----------
        job_identifier : Job identifier.
        data : POST HTTP request's data.
        json : POST HTTP request's json data.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{job_identifier}/resume',
            data=data,
            json=json,
            **kwargs)

    def get_job_output(
            self, job_identifier: str,
            key: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get outputs generated by the job

        Retrieve outputs generated by the job (only valid after job is successful).

        Parameters
        ----------
        job_identifier : Job identifier.
        key : Key to get output
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Outputs generated by the job.
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs/{job_identifier}/{key}',
            params=params,
            **kwargs)

    def get_remote_modalities(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get remotes modalities

        List registered modalities (remote PACS servers that are connected to Orthanc)
        See the Orthanc's config for more details (AET addresses).

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of modalities.
        """
        return self.get_request(
            f'{self._orthanc_url}/modalities', params=params, **kwargs)

    def get_remote_modality(
            self, remote_modality: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get specified remote modality

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/modalities/{remote_modality}', params=params, **kwargs)

    def delete_remote_modality(self, remote_modality: str, **kwargs) -> requests.Response:
        """Delete remote modality

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/modalities/{remote_modality}',
                                   **kwargs)

    def put_remote_modality(
            self, remote_modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put remote modality

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/modalities/{remote_modality}',
            data=data,
            json=json,
            **kwargs)

    def echo_to_remote_modality(
            self, remote_modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Test connection to remote modality (C-Echo SCU)

        C-Echo SCU.

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Echo succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{remote_modality}/echo',
            data=data,
            json=json,
            **kwargs)

    def move_from_remote_modality(
            self, remote_modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Move (C-Move SCU) specified query.

        DICOM C-Move SCU (Retrieve).

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Move succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{remote_modality}/move',
            data=data,
            json=json,
            **kwargs)

    def query_on_remote_modality(
            self, remote_modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Query on remote modalities

        DICOM C-Find SCU (Query), with subsequent possibility for Retrieve.
        See http://book.orthanc-server.com/users/rest.html#performing-queries-on-modalities.

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Result of query in the form of { "ID": "{query-id}", "Path": "/queries/{query-id}" }

        Examples
        --------
        >>> orthanc = Orthanc('http://localhost:8042')
        >>> orthanc.query_on_remote_modality('remote_modality',
        ...                                    data={'Level': 'Study',
        ...                                          'Query': {
        ...                                             'QueryRetrieveLevel': 'Study',
        ...                                             'Modality':'SR'}})

        >>> orthanc.retrieve_from_remote_modality('remote_modality')  # TODO
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{remote_modality}/query',
            data=data,
            json=json,
            **kwargs)

    def store_on_remote_modality(
            self, remote_modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Store data on remote modality (C-Store).

        POST body = UUID series, UUID instance, or raw DICOM file.

        Parameters
        ----------
        remote_modality : Remote modality (remote PACS server, see orthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Move succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{remote_modality}/store',
            data=data,
            json=json,
            **kwargs)

    def get_patients(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get patient identifiers

        "since" and "limit" arguments + "expand" argument to retrieve the content of the patients.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of patient identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients', params=params, **kwargs)

    def get_patient_main_information(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient mains information

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Dictionary of patient main information.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}',
            params=params,
            **kwargs)

    def delete_patient(self, patient_identifier: str, **kwargs) -> requests.Response:
        """Delete specified patient

        Parameters
        ----------
        patient_identifier : Patient identifier.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then deletion has succeeded.
        """
        return self.delete_request(
            f'{self._orthanc_url}/patients/{patient_identifier}', **kwargs)

    def anonymize_patient(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Anonymize specified patient

        http://book.orthanc-server.com/users/anonymization.html

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then anonymization has succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_archive(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create ZIP.

        Parameters
        ----------
        patient_identifier : Patient identifier.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/archive',
            params=params,
            **kwargs)

    def post_patients_identifier_archive(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create ZIP

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_instances(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the instances of this patient in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/instances',
            params=params,
            **kwargs)

    def get_patients_identifier_instances_tags(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_patients_identifier_media(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/media',
            params=params,
            **kwargs)

    def post_patients_identifier_media(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_patients_identifier_modify(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        http://book.orthanc-server.com/users/anonymization.html

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_module(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/module',
            params=params,
            **kwargs)

    def get_patients_identifier_protected(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Protection against recycling: "0" means unprotected, "1" protected

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/protected',
            params=params,
            **kwargs)

    def put_patients_identifier_protected(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put method

         Protection against recycling: "0" means unprotected, "1" protected

         Returns
         -------
         requests.Response
         """
        return self.put_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/protected',
            data=data,
            json=json,
            **kwargs)

    def post_patients_identifier_reconstruct(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_series(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the series of this patient in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/series',
            params=params,
            **kwargs)

    def get_patients_identifier_shared_tags(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/shared_tags',
            params=params,
            **kwargs)

    def get_patients_identifier_statistics(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/statistics',
            params=params,
            **kwargs)

    def get_patients_identifier_studies(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the studies of this patient in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/studies',
            params=params,
            **kwargs)

    def get_peers(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/peers', params=params, **kwargs)

    def get_peers_peer(self, peer: str, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/peers/{peer}', params=params, **kwargs)

    def delete_peers_peer(self, peer: str, **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/peers/{peer}',
                                   **kwargs)

    def put_peers_peer(self, peer: str, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Put method

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/peers/{peer}',
            data=data,
            json=json,
            **kwargs)

    def post_peers_peer_store(
            self, peer: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        POST body = UUID series, UUID instance, or raw DICOM file

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/peers/{peer}/store',
            data=data,
            json=json,
            **kwargs)

    def get_plugins(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Get the list of all the registered plugins

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins', params=params, **kwargs)

    def get_plugins_identifier(
            self,
            plugin_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Get information about some plugin

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/{plugin_identifier}',
            params=params,
            **kwargs)

    def get_plugins_explorer_js(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Get the JavaScript code that is injected by plugins into Orthanc Explorer

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/explorer.js',
            params=params,
            **kwargs)

    def get_queries(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries', params=params, **kwargs)

    def get_queries_identifier(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}',
            params=params,
            **kwargs)

    def delete_queries_identifier(self, query_identifier: str, **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/queries/{query_identifier}',
                                   **kwargs)

    def get_queries_identifier_answers(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        List all the answers for this C-Find SCU request
         ("?expand" to show content, "&simplify" to simplify output)

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers',
            params=params,
            **kwargs)

    def get_queries_identifier_answers_index_content(
            self, query_identifier: str,
            index: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Access 1 answer of C-Find SCU; "?simplify" argument to simplify output

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/content',
            params=params,
            **kwargs)

    def post_queries_identifier_answers_index_retrieve(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        C-Move SCU: Send this resource to another modality whose AET is in the body

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_instances(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Launch another C-Find SCU to find the child DICOM instances of the given answer (might not work with all PACS)

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query_instances',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_series(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Launch another C-Find SCU to find the child series of the given answer

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query_series',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_studies(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Launch another C-Find SCU to find the child patient of the given answer

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query_studies',
            data=data,
            json=json,
            **kwargs)

    def get_queries_identifier_level(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Get the query retrieve level for this C-Find SCU request

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/level',
            params=params,
            **kwargs)

    def get_queries_identifier_modality(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Get the modality to which this C-Find SCU request was issued (cf. /modalities)

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/modality',
            params=params,
            **kwargs)

    def get_queries_identifier_query(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Access the C-Find SCU query; "?simplify" argument to simplify output

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/query',
            params=params,
            **kwargs)

    def post_queries_identifier_retrieve(
            self, query_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Returns
        -------
        requests.Response

        Examples
        --------
        >>> orthanc = Orthanc('http://localhost:8042')
        >>> orthanc.query_on_remote_modality('remote_modality',
        ...                                    data={'Level': 'Study',
        ...                                          'Query': {
        ...                                             'QueryRetrieveLevel': 'Study',
        ...                                             'Modality':'SR'}})

        >>> orthanc.retrieve_from_remote_modality('remote_modality')

        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def get_series(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        "since" and "limit" arguments + "expand" argument to retrieve the content of the series

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series', params=params, **kwargs)

    def get_series_identifier(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}',
            params=params,
            **kwargs)

    def delete_series_identifier(self, series_identifier: str, **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/series/{series_identifier}',
                                   **kwargs)

    def post_series_identifier_anonymize(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        http://book.orthanc-server.com/users/anonymization.html

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_archive(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/archive',
            params=params,
            **kwargs)

    def post_series_identifier_archive(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_instances(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the instances of this series in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/instances',
            params=params,
            **kwargs)

    def get_series_identifier_instances_tags(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_series_identifier_media(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create archives for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/media',
            params=params,
            **kwargs)

    def post_series_identifier_media(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create archives for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_series_identifier_modify(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        http://book.orthanc-server.com/users/anonymization.html

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_module(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/module',
            params=params,
            **kwargs)

    def get_series_identifier_ordered_slices(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Order the slices of a 2D+t, 3D or 3D+t image

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/ordered_slices',
            params=params,
            **kwargs)

    def get_series_identifier_patient(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve the parent patient of this series

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/patient',
            params=params,
            **kwargs)

    def post_series_identifier_reconstruct(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_shared_tags(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/shared_tags',
            params=params,
            **kwargs)

    def get_series_identifier_statistics(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/statistics',
            params=params,
            **kwargs)

    def get_series_identifier_study(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve the parent study of this series

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/study',
            params=params,
            **kwargs)

    def get_statistics(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/statistics', params=params, **kwargs)

    def get_studies(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        "since" and "limit" arguments + "expand" argument to retrieve the content of the studies

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies', params=params, **kwargs)

    def get_studies_identifier(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}',
            params=params,
            **kwargs)

    def delete_studies_identifier(self, study_identifier: str, **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/studies/{study_identifier}',
                                   **kwargs)

    def post_studies_identifier_anonymize(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        http://book.orthanc-server.com/users/anonymization.html

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_archive(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create ZIP

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/archive',
            params=params,
            **kwargs)

    def post_studies_identifier_archive(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create ZIP

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_instances(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the instances of this patient in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/instances',
            params=params,
            **kwargs)

    def get_studies_identifier_instances_tags(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_studies_identifier_media(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/media',
            params=params,
            **kwargs)

    def post_studies_identifier_media(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create a ZIP archive for media storage with DICOMDIR

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_studies_identifier_merge(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Merge a study, i.e. move series from another study into this study

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/merge',
            data=data,
            json=json,
            **kwargs)

    def post_studies_identifier_modify(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        http://book.orthanc-server.com/users/anonymization.html

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_module(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/module',
            params=params,
            **kwargs)

    def get_studies_identifier_module_patient(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/module_patient',
            params=params,
            **kwargs)

    def get_studies_identifier_patient(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve the parent patient of this study

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/patient',
            params=params,
            **kwargs)

    def post_studies_identifier_reconstruct(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_series(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Retrieve all the series of this study in a single REST call

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/series',
            params=params,
            **kwargs)

    def get_studies_identifier_shared_tags(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?simplify" argument to simplify output, "?short"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/shared_tags',
            params=params,
            **kwargs)

    def post_studies_identifier_split(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Split a study, i.e. create a new study from a subset of its child series

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/split',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_statistics(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/statistics',
            params=params,
            **kwargs)

    def get_system(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/system', params=params, **kwargs)

    def post_tools_create_archive(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Create a ZIP from a set of unrelated DICOM resources

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_archive',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_dicom(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Create and store a new DICOM instance,
        possibly with an image or a PDF payload

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_dicom',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_media(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_media_extended(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources, including type-3 tags

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media_extended',
            data=data,
            json=json,
            **kwargs)

    def get_tools_default_encoding(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Get the default encoding used by Orthanc, or temporarily change it until the next restart

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/default_encoding',
            params=params,
            **kwargs)

    def put_tools_default_encoding(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put method

        Get the default encoding used by Orthanc, or temporarily change it until the next restart

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/default_encoding',
            data=data,
            json=json,
            **kwargs)

    def get_tools_dicom_conformance(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        DICOM conformance statement of this version of Orthanc

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/dicom_conformance',
            params=params,
            **kwargs)

    def post_tools_execute_script(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Execute the Lua script in the POST body

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/execute_script',
            data=data,
            json=json,
            **kwargs)

    def post_tools_find(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Runs a C-Find call from the REST API

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/find', data=data, json=json, **kwargs)

    def get_tools_generate_uid(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Generate DICOM UID. The "level" GET argument must be "patient", "study", "series" or "instance"

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/generate_uid', params=params, **kwargs)

    def post_tools_invalidate_tags(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Invalidate the JSON summary of all the DICOM files (useful if new private tags are registered)

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/invalidate_tags',
            data=data,
            json=json,
            **kwargs)

    def post_tools_lookup(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Map DICOM UIDs to Orthanc identifiers

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/lookup',
            data=data,
            json=json,
            **kwargs)

    def get_tools_metrics(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        See whether the collection of metrics is enabled, and enable/disable this collection

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics', params=params, **kwargs)

    def put_tools_metrics(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Put method

        See whether the collection of metrics is enabled, and enable/disable this collection

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/metrics',
            data=data,
            json=json,
            **kwargs)

    def get_tools_metrics_prometheus(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Retrieve the metrics in the Prometheus text-based exposition format

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics_prometheus',
            params=params,
            **kwargs)

    def get_tools_now(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns the current *universal* datetime (UTC) in the ISO 8601 format

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now', params=params, **kwargs)

    def get_tools_now_local(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns the current *local* datetime in the ISO 8601 format

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now_local', params=params, **kwargs)

    def post_tools_reconstruct(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Reconstructs the main DICOM tags, the JSON summary and metadata of
         all the instances stored in Orthanc. Slow operation!

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def post_tools_reset(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Hot restart of Orthanc, the configuration file will be read again

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reset', data=data, json=json, **kwargs)

    def post_tools_shutdown(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Post method

        Stop Orthanc

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/shutdown',
            data=data,
            json=json,
            **kwargs)
