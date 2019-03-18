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

    def __init__(self, orthanc_url: str) -> None:
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
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed-data',
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
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed-md5',
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
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed-size',
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
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/is-compressed',
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
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/verify-md5',
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

    def get_instance_information(
            self, instance_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get instance information

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

        http://book.pyorthanc-server.com/users/anonymization.html

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

    def get_instance_content_by_group_element(
            self, instance_identifier: str,
            group_element: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get value of DICOM tags corresponding to a specified group element

        Raw access to the value of DICOM tags (comprising the padding character).
        Group element name should be in the form {tag1}/{index1}/{tag2}/...

        Parameters
        ----------
        instance_identifier : Instance identifier.
        group_element : Group element corresponding to targeted DICOM tag.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            DICOM tag value.

        Examples
        --------
        >>> pyorthanc = Orthanc('http://localhost:8080')
        >>> pyorthanc.get_instance_content_by_group_element(
        ...     '0040-a730/6/0040-a730/0/0040-a160').json()
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{instance_identifier}/content/{group_element}',
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
        instance_identifier : Instance identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Bytes corresponding to DICOM file.

        Examples
        --------
        >>> pyorthanc = Orthanc('ORTHANC_URL')
        >>> dicom_file_bytes = pyorthanc.get_instance_file('an_instance_identifier').json()
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
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image-int16',
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
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image-uint16',
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
            f'{self._orthanc_url}/instances/{instance_identifier}/frames/{frame_number}/image-uint8',
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
            f'{self._orthanc_url}/instances/{instance_identifier}/image-int16',
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
            f'{self._orthanc_url}/instances/{instance_identifier}/image-uint16',
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
            f'{self._orthanc_url}/instances/{instance_identifier}/image-uint8',
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

        See http://book.pyorthanc-server.com/users/anonymization.html .

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
        """Reconstruction of the main DICOM tags of instance

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
            f'{self._orthanc_url}/instances/{instance_identifier}/simplified-tags',
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

    def get_modalities(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get modalities

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

    def get_modality(
            self, modality: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get specified modality

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/modalities/{modality}', params=params, **kwargs)

    def delete_modality(self, modality: str, **kwargs) -> requests.Response:
        """Delete remote modality

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/modalities/{modality}',
                                   **kwargs)

    def put_modality(
            self, modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put remote modality

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/modalities/{modality}',
            data=data,
            json=json,
            **kwargs)

    def echo_to_modality(
            self, modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Test connection to remote modality (C-Echo SCU)

        C-Echo SCU.

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Echo succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{modality}/echo',
            data=data,
            json=json,
            **kwargs)

    def move_from_modality(
            self, modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Move (C-Move SCU) specified query.

        DICOM C-Move SCU (Retrieve).

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Move succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{modality}/move',
            data=data,
            json=json,
            **kwargs)

    def query_on_modality(
            self, modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Query on remote modalities

        DICOM C-Find SCU (Query), with subsequent possibility for Retrieve.
        See http://book.pyorthanc-server.com/users/rest.html#performing-queries-on-modalities.

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Result of query in the form of { "ID": "{query-id}", "Path": "/queries/{query-id}" }

        Examples
        --------
        >>> pyorthanc = Orthanc('http://localhost:8042')
        >>> pyorthanc.query_on_modality('modality',
        ...                                    data={'Level': 'Study',
        ...                                          'Query': {
        ...                                             'QueryRetrieveLevel': 'Study',
        ...                                             'Modality':'SR'}}).json()

        >>> pyorthanc.retrieve_query_results_to_another_modality('modality')
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{modality}/query',
            data=data,
            json=json,
            **kwargs)

    def store_on_modality(
            self, modality: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Store data on remote modality (C-Store).

        POST body = UUID series, UUID instance, or raw DICOM file.

        Parameters
        ----------
        modality : Modality (remote PACS server, see pyorthanc.get_modalities()).
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then C-Move succeeded.
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{modality}/store',
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

    def get_patient_information(
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

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then anonymization doesn't encounter error.
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_patient_zip(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get the

        Get the .zip file.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Zip file of the patient.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/archive',
            params=params,
            **kwargs)

    def archive_patient(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Archive patient

        Create ZIP.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            If HTTP status == 200 then anonymization doesn't encounter error.
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_patient_instances(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient instances

        Retrieve all the instances of this patient in a single REST call.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Patient instance.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/instances',
            params=params,
            **kwargs)

    def get_patient_instances_tags(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get tags of all patient instances

        "?simplify" argument to simplify output, "?short"

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Patient instances tags.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/instances-tags',
            params=params,
            **kwargs)

    def get_patient_archice(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient zip archive for media storage with DICOMDIR

        Create a ZIP archive for media storage with DICOMDIR.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/media',
            params=params,
            **kwargs)

    def create_patient_archive_for_media_storage(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create patient archive media with DICOMDIR

        Create a ZIP archive for media storage with DICOMDIR.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def modify_patient(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Modify patient

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_patient_module(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient module

        "?simplify" argument to simplify output, "?short"

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/module',
            params=params,
            **kwargs)

    def get_if_patient_is_protected(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get if patient is protected against recycling

        Protection against recycling: "0" means unprotected, "1" protected.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Protection against recycling: "0" means unprotected, "1" protected.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/protected',
            params=params,
            **kwargs)

    def set_patient_protected_or_not(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Set patient as protected or not

        Protection against recycling: "0" means unprotected, "1" protected

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.put_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/protected',
            data=data,
            json=json,
            **kwargs)

    def reconstruct_main_dicom_tags_of_patient(
            self, patient_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Force reconstruction of the main DICOM tags of patient

        Force reconstruction of the main DICOM tags,
        JSON summary and metadata of child instances

        Parameters
        ----------
        patient_identifier : Patient identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_patient_series(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient series identifiers

        Retrieve all the series of this patient in a single REST call.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of series identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/series',
            params=params,
            **kwargs)

    def get_patient_shared_tags(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient shared tags

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/shared-tags',
            params=params,
            **kwargs)

    def get_patient_statistics(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient statistics

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/statistics',
            params=params,
            **kwargs)

    def get_patient_studies(
            self, patient_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get patient studies identifiers

        Retrieve all the studies of this patient in a single REST call.

        Parameters
        ----------
        patient_identifier : Patient identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of patient studies identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{patient_identifier}/studies',
            params=params,
            **kwargs)

    def get_peers(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get peers

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Peers.
        """
        return self.get_request(
            f'{self._orthanc_url}/peers', params=params, **kwargs)

    def get_peer(
            self, peer_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get peer

        Parameters
        ----------
        peer_identifier : Peer identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/peers/{peer_identifier}', params=params, **kwargs)

    def delete_peers_peer(self, peer_identifier: str, **kwargs) -> requests.Response:
        """Delete specified peer

        Parameters
        ----------
        peer_identifier : Peer identifier.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.delete_request(f'{self._orthanc_url}/peers/{peer_identifier}',
                                   **kwargs)

    def put_peer(
            self, peer_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put peer

        Parameters
        ----------
        peer_identifier : Peer identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/peers/{peer_identifier}',
            data=data,
            json=json,
            **kwargs)

    def store_peer(
            self, peer_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        POST body = UUID series, UUID instance, or raw DICOM file

        Parameters
        ----------
        peer_identifier : Peer identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/peers/{peer_identifier}/store',
            data=data,
            json=json,
            **kwargs)

    def get_plugins(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get plugin names/identifiers

        Get the list of all the registered plugins

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of registered plugin names/identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins', params=params, **kwargs)

    def get_plugin(
            self,
            plugin_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get specified plugin information

        Get information about specified plugin.

        Parameters
        ----------
        plugin_identifier : Plugin identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Plugin information.
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/{plugin_identifier}',
            params=params,
            **kwargs)

    def get_plugins_js_code(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get the javascript code injected by plugins

        Get the JavaScript code that is injected by plugins into Orthanc Explorer.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/explorer.js',
            params=params,
            **kwargs)

    def get_queries(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get queries

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of queries.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries', params=params, **kwargs)

    def get_queries_information(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get specified query information

        Parameters
        ----------
        query_identifier : Query identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Query information.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}',
            params=params,
            **kwargs)

    def delete_query(self, query_identifier: str, **kwargs) -> requests.Response:
        """Delete specified query

        Parameters
        ----------
        query_identifier : Query identifier.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.delete_request(f'{self._orthanc_url}/queries/{query_identifier}',
                                   **kwargs)

    def get_query_answers(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get query answers

        List all the answers for this C-Find SCU request
         ("?expand" to show content, "&simplify" to simplify output)

        Parameters
        ----------
        query_identifier : Query identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List all the answers for the specified query.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers',
            params=params,
            **kwargs)

    def get_content_of_specified_query_answer(
            self, query_identifier: str,
            index: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get content of specified answer of C-Find

        Access 1 answer of C-Find SCU; "?simplify" argument to simplify output.

        Parameters
        ----------
        query_identifier : Query identifier.
        index : Index of wanted answer.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Specified answer of C-Find SCU operation.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/content',
            params=params,
            **kwargs)

    def send_resource_to_other_modality(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """(C-Move) Send resource to another modality with AET in request body

        C-Move SCU: Send this resource to another modality whose AET is in the body.

        Parameters
        ----------
        query_identifier : Query identifier.
        index : Index of wanted answer.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def find_child_dicom_instances_of_answer(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Find child dicom instances of answer

        Launch another C-Find SCU to find the child DICOM instances of
         the given answer (might not work with all PACS).

        Parameters
        ----------
        query_identifier : Query identifier.
        index : Index of wanted answer.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query-instances',
            data=data,
            json=json,
            **kwargs)

    def find_child_dicom_series_of_answer(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Find child dicom series of answer

        Launch another C-Find SCU to find the child series of the given answer.

        Parameters
        ----------
        query_identifier : Query identifier.
        index : Index of wanted answer.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query-series',
            data=data,
            json=json,
            **kwargs)

    def find_child_dicom_studies_of_answer(
            self, query_identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Find child dicom studies of answer

        Launch another C-Find SCU to find the child patient of the given answer.

        Parameters
        ----------
        query_identifier : Query identifier.
        index : Index of wanted answer.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/answers/{index}/query-studies',
            data=data,
            json=json,
            **kwargs)

    def get_query_retrieve_level(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get query retrieve level

        Get the query retrieve level for this C-Find SCU request.

        Parameters
        ----------
        query_identifier : Query identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Query retrieve level for this C-Find SCU request
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/level',
            params=params,
            **kwargs)

    def get_query_modality(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get the modality to which this C-Find SCU request was issued

        Get the modality to which this C-Find SCU request was issued (cf. /modalities)

        Parameters
        ----------
        query_identifier : Query identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Modality to which this C-Find SCU request was issued.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/modality',
            params=params,
            **kwargs)

    def get_query_information(
            self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get access query

        Access the C-Find SCU query; "?simplify" argument to simplify output.

        Parameters
        ----------
        query_identifier : Query identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Query information.
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{query_identifier}/query',
            params=params,
            **kwargs)

    def retrieve_query_results_to_another_modality(
            self, query_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Retrieve (C-Move) query results to another modality

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        query_identifier : Query identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response

        Examples
        --------
        >>> pyorthanc = Orthanc('http://localhost:8042')
        >>> query_id = pyorthanc.query_on_modality(
        ...     'modality',
        ...     data={'Level': 'Study',
        ...           'Query': {'QueryRetrieveLevel': 'Study',
        ...                     'Modality':'SR'}}).json()

        >>> pyorthanc.retrieve_query_results_to_another_modality(
        ...         query_identifier=query_id['ID'],
        ...         json='modality')

        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{query_identifier}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def get_series(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get series identifiers

        "since" and "limit" arguments + "expand" argument to retrieve the content of the series.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of series identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/series', params=params, **kwargs)

    def get_series_information(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series information

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series main information in the form of dictionary.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}',
            params=params,
            **kwargs)

    def delete_series(self, series_identifier: str, **kwargs) -> requests.Response:
        """Delete specified series

        Parameters
        ----------
        series_identifier : Series identifier.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.delete_request(f'{self._orthanc_url}/series/{series_identifier}',
                                   **kwargs)

    def anonymize_series(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Anonymize series

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        series_identifier : Series identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_series_zip_file(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series zip file

        Get a ZIP archive for media storage with DICOMDIR.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series zip file.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/archive',
            params=params,
            **kwargs)

    def create_series_zip_file(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create series zip file

        Create a ZIP archive for media storage with DICOMDIR.

        Parameters
        ----------
        series_identifier : Series identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_series_instances(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series instances

        Retrieve all the instances of this series in a single REST call.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of series instances.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/instances',
            params=params,
            **kwargs)

    def get_series_instances_tags(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series instances tags

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of series instances tags.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/instances-tags',
            params=params,
            **kwargs)

    def get_series_archives(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series media storage with DICOMDIR

        Get archives for media storage with DICOMDIR.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/media',
            params=params,
            **kwargs)

    def create_series_archive_for_media_storage(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create archive for media storage

        Create archives for media storage with DICOMDIR.

        Parameters
        ----------
        series_identifier : Series identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_series_modify(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Modify series

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        series_identifier : Series identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_series_module(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series module

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series module.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/module',
            params=params,
            **kwargs)

    def get_series_ordered_slices(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series ordered slices

        Order the slices of a 2D+t, 3D or 3D+t image.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/ordered-slices',
            params=params,
            **kwargs)

    def get_series_patient_identifier(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series patient identifier

        Retrieve the parent patient of this series.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Patient identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/patient',
            params=params,
            **kwargs)

    def reconstruct_main_dicom_tags_of_series(
            self, series_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Reconstruction of the main DICOM tags of series

        Force reconstruction of the main DICOM tags,
        JSON summary and metadata of child instances

        Parameters
        ----------
        series_identifier : Series identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{series_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_series_shared_tags(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series shared tags

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/shared-tags',
            params=params,
            **kwargs)

    def get_series_statistics(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series statistics

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series statistics.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/statistics',
            params=params,
            **kwargs)

    def get_series_study_identifier(
            self, series_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get series study identifier

        Retrieve the parent study of this series.

        Parameters
        ----------
        series_identifier : Series identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Series study identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{series_identifier}/study',
            params=params,
            **kwargs)

    def get_statistics(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get Orthanc statistics

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Orthanc statistics.
        """
        return self.get_request(
            f'{self._orthanc_url}/statistics', params=params, **kwargs)

    def get_studies(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get studies identifiers

        "since" and "limit" arguments + "expand" argument to retrieve the content of the studies.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of the studies identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies', params=params, **kwargs)

    def get_study_information(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study information

        Parameters
        ----------
        study_identifier : studies identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study main information in the form of a dictionary.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}',
            params=params,
            **kwargs)

    def delete_study(self, study_identifier: str, **kwargs) -> requests.Response:
        """Delete specified study

        Parameters
        ----------
        study_identifier : studies identifier.

        Returns
        -------
        requests.Response
            HTTP status == 200 if no error.
        """
        return self.delete_request(f'{self._orthanc_url}/studies/{study_identifier}',
                                   **kwargs)

    def anonymize_study(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Anonymize study

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        study_identifier : studies identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_study_zip_file(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study zip file

        Get ZIP file

        Parameters
        ----------
        study_identifier : studies identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/archive',
            params=params,
            **kwargs)

    def create_study_zip_file(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create study zip file

        Create ZIP.

        Parameters
        ----------
        study_identifier : studies identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_study_instances(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study instances

        Retrieve all the instances of this patient in a single REST call.

        Parameters
        ----------
        study_identifier : studies identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of study instances.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/instances',
            params=params,
            **kwargs)

    def get_study_instances_tags(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study instances tags

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        study_identifier : studies identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/instances-tags',
            params=params,
            **kwargs)

    def get_study_archive(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study archive

        Parameters
        ----------
        study_identifier : studies identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/media',
            params=params,
            **kwargs)

    def create_study_archive_for_media_storage(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create archive for media storage

        Create a ZIP archive for media storage with DICOMDIR.

        Parameters
        ----------
        study_identifier : Study identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def merge_study(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Merge study

        Merge a study, i.e. move series from another study into this study

        Parameters
        ----------
        study_identifier : Study identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/merge',
            data=data,
            json=json,
            **kwargs)

    def modify_study(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Modify study

        http://book.pyorthanc-server.com/users/anonymization.html

        Parameters
        ----------
        study_identifier : Study identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_study_module(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study module

        "?simplify" argument to simplify output, "?short".

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study module
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/module',
            params=params,
            **kwargs)

    def get_study_module_patient(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study's module_patient

        "?simplify" argument to simplify output, "?short"

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study's module_patient
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/module-patient',
            params=params,
            **kwargs)

    def get_study_patient_identifier(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study's patient identifier

        Retrieve the parent patient of this study

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study's patient identifier.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/patient',
            params=params,
            **kwargs)

    def reconstruct_study_main_dicom_tags(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Reconstruct the main DICOM tags of study

        Force reconstruction of the main DICOM tags,
        JSON summary and metadata of child instances

        Parameters
        ----------
        study_identifier : Study identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_study_series_identifiers(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study's series identifiers

        Retrieve all the series of this study in a single REST call.

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of study's series identifiers.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/series',
            params=params,
            **kwargs)

    def get_study_shared_tags(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study's shared tags

        "?simplify" argument to simplify output, "?short"

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study's shared tags.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/shared-tags',
            params=params,
            **kwargs)

    def split_study(
            self, study_identifier: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Split study

        Split a study, i.e. create a new study from a subset of its child series.

        Parameters
        ----------
        study_identifier : Study identifier.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{study_identifier}/split',
            data=data,
            json=json,
            **kwargs)

    def get_study_statistics(
            self, study_identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get study statistics

        Parameters
        ----------
        study_identifier : Study identifier.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Study statistics.
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{study_identifier}/statistics',
            params=params,
            **kwargs)

    def get_system(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get system

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/system', params=params, **kwargs)

    def create_archive(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Create archive (ZIP) from specified set of DICOM objects

        Create a ZIP from a set of unrelated DICOM resources

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_archive',
            data=data,
            json=json,
            **kwargs)

    def create_and_store_dicom(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Create and store new DICOM instance

        Create and store a new DICOM instance,
        possibly with an image or a PDF payload

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_dicom',
            data=data,
            json=json,
            **kwargs)

    def create_media(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Create a ZIP with DICOMDIR from specified DICOM objects

        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media',
            data=data,
            json=json,
            **kwargs)

    def create_media_extended_to_type3(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Create a ZIP with DICOMDIR from specified DICOM objects (this include type-3 tags)

        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources,
        including type-3 tags.

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media-extended',
            data=data,
            json=json,
            **kwargs)

    def get_default_encoding(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get default encoding

        Get the default encoding used by Orthanc.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Default Encoding.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/default_encoding',
            params=params,
            **kwargs)

    def put_default_encoding(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Change the default encoding

        Temporarily change the default encoding until the next restart.

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/default_encoding',
            data=data,
            json=json,
            **kwargs)

    def get_dicom_conformance(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get DICOM conformance statement of this version of Orthanc

        DICOM conformance statement of this version of Orthanc.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            DICOM conformance statement of this version of Orthanc.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/dicom_conformance',
            params=params,
            **kwargs)

    def execute_given_script(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Execute given script

        Execute the Lua script in the POST body.

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/execute-script',
            data=data,
            json=json,
            **kwargs)

    def c_find(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """C-Find call

        Runs a C-Find call from the REST API

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/find', data=data, json=json, **kwargs)

    def generate_uid(self, params: Dict = None, **kwargs) -> requests.Response:
        """Generate a DICOM UID

        Generate DICOM UID. The "level" GET argument must be "patient", "study", "series" or "instance"

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            DICOM UID.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/generate-uid', params=params, **kwargs)

    def invalidate_tags(
            self, data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Invalidate the JSON summary of all DICOM files

        Invalidate the JSON summary of all the DICOM files
        (useful if new private tags are registered).

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/invalidate-tags',
            data=data,
            json=json,
            **kwargs)

    def lookup(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Map DICOM UIDs to Orthanc identifiers

        Map DICOM UIDs to Orthanc identifiers

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/lookup',
            data=data,
            json=json,
            **kwargs)

    def get_metrics(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get metrics

        See whether the collection of metrics is enabled.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Metrics
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics', params=params, **kwargs)

    def put_metrics(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Put method

        Enable/disable this collection of metrics

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/metrics',
            data=data,
            json=json,
            **kwargs)

    def get_metrics_prometheus(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get metrics in the Prometheus text-based exposition format

        Retrieve the metrics in the Prometheus text-based exposition format.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Metrics in the Prometheus text-based exposition format.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics-prometheus',
            params=params,
            **kwargs)

    def get_universal_time(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get universal current time

        Returns the current *universal* datetime (UTC) in the ISO 8601 format.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Universal current time.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now', params=params, **kwargs)

    def get_local_time(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get local current time

        Returns the current *local* datetime in the ISO 8601 format.

        Parameters
        ----------
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Local current time.
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now-local', params=params, **kwargs)

    def reconstruct_main_dicom_tags(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Reconstruct main DICOM tags

        Reconstructs the main DICOM tags, the JSON summary and metadata of
         all the instances stored in Orthanc. Slow operation!

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def reset_orthanc(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Hot restart of Orthanc

        Hot restart of Orthanc, the configuration file will be read again

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reset', data=data, json=json, **kwargs)

    def shutdown_orthanc(self, data: Dict = None, json=None, **kwargs) -> requests.Response:
        """Shutdown Orthanc

        Stop Orthanc.

        Parameters
        ----------
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/shutdown',
            data=data,
            json=json,
            **kwargs)
