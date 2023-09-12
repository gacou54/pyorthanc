try:
    from orthanc import *

except ModuleNotFoundError:
    """Orthanc SDK methods wrapped in python (plugin version 4.0)"""
    import warnings

    from enum import Enum
    from typing import Any, Callable

    warnings.warn('Cannot import orthanc sdk. Using mock instead.')

    VERSION = '4.0'

    class ChangeType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginChangeType"""
        COMPLETED_SERIES = 0
        DELETED = 1
        JOB_FAILURE = 18
        JOB_SUBMITTED = 16
        JOB_SUCCESS = 17
        NEW_CHILD_INSTANCE = 2
        NEW_INSTANCE = 3
        NEW_PATIENT = 4
        NEW_SERIES = 5
        NEW_STUDY = 6
        ORTHANC_STARTED = 10
        ORTHANC_STOPPED = 11
        STABLE_PATIENT = 7
        STABLE_SERIES = 8
        STABLE_STUDY = 9
        UPDATED_ATTACHMENT = 12
        UPDATED_METADATA = 13
        UPDATED_MODALITIES = 15
        UPDATED_PEERS = 14


    class CompressionType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginCompressionType"""
        GZIP = 2
        GZIP_WITH_SIZE = 3
        ZLIB = 0
        ZLIB_WITH_SIZE = 1


    class ConstraintType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginConstraintType"""
        EQUAL = 1
        GREATER_OR_EQUAL = 3
        LIST = 5
        SMALLER_OR_EQUAL = 2
        WILDCARD = 4


    class ContentType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginContentType"""
        DICOM = 1
        DICOM_AS_JSON = 2
        DICOM_UNTIL_PIXEL_DATA = 3
        UNKNOWN = 0


    class CreateDicomFlags(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginCreateDicomFlags"""
        DECODE_DATA_URI_SCHEME = 1
        GENERATE_IDENTIFIERS = 2
        NONE = 0


    class DicomToJsonFlags(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginDicomToJsonFlags"""
        CONVERT_BINARY_TO_ASCII = 16
        CONVERT_BINARY_TO_NULL = 32
        INCLUDE_BINARY = 1
        INCLUDE_PIXEL_DATA = 8
        INCLUDE_PRIVATE_TAGS = 2
        INCLUDE_UNKNOWN_TAGS = 4
        NONE = 0
        SKIP_GROUP_LENGTHS = 128
        STOP_AFTER_PIXEL_DATA = 64


    class DicomToJsonFormat(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginDicomToJsonFormat"""
        FULL = 1
        HUMAN = 3
        SHORT = 2


    class DicomWebBinaryMode(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginDicomWebBinaryMode"""
        BULK_DATA_URI = 2
        IGNORE = 0
        INLINE_BINARY = 1


    class DicomWebNode:
        """Generated from Orthanc C class: OrthancPluginDicomWebNode"""


    class ErrorCode(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginErrorCode"""
        ALREADY_EXISTING_TAG = 2042
        BAD_APPLICATION_ENTITY_TITLE = 2009
        BAD_FILE_FORMAT = 15
        BAD_FONT = 30
        BAD_GEOMETRY = 38
        BAD_HTTP_STATUS_IN_REST = 2005
        BAD_JOB_ORDERING = 2028
        BAD_JSON = 28
        BAD_PARAMETER_TYPE = 5
        BAD_RANGE = 41
        BAD_REQUEST = 8
        BAD_SEQUENCE_OF_CALLS = 6
        CANCELED_JOB = 37
        CANNOT_CREATE_LUA = 2030
        CANNOT_EXECUTE_LUA = 2031
        CANNOT_ORDER_SLICES = 2040
        CANNOT_STORE_INSTANCE = 2018
        CANNOT_WRITE_FILE = 14
        CORRUPTED_FILE = 20
        CREATE_DICOM_BAD_PARENT = 2024
        CREATE_DICOM_NOT_STRING = 2019
        CREATE_DICOM_NO_PAYLOAD = 2022
        CREATE_DICOM_OVERRIDE_TAG = 2020
        CREATE_DICOM_PARENT_ENCODING = 2026
        CREATE_DICOM_PARENT_IS_INSTANCE = 2025
        CREATE_DICOM_USE_CONTENT = 2021
        CREATE_DICOM_USE_DATA_URI_SCHEME = 2023
        DATABASE = 11
        DATABASE_BACKEND_ALREADY_REGISTERED = 2037
        DATABASE_CANNOT_SERIALIZE = 42
        DATABASE_NOT_INITIALIZED = 2038
        DATABASE_PLUGIN = 31
        DATABASE_UNAVAILABLE = 36
        DICOM_FIND_UNAVAILABLE = 2016
        DICOM_MOVE_UNAVAILABLE = 2017
        DICOM_PORT_IN_USE = 2004
        DIRECTORY_EXPECTED = 2002
        DIRECTORY_OVER_FILE = 2000
        DISCONTINUED_ABI = 40
        EMPTY_REQUEST = 33
        FILE_STORAGE_CANNOT_WRITE = 2001
        FULL_STORAGE = 19
        HTTP_PORT_IN_USE = 2003
        INCOMPATIBLE_DATABASE_VERSION = 18
        INCOMPATIBLE_IMAGE_FORMAT = 23
        INCOMPATIBLE_IMAGE_SIZE = 24
        INEXISTENT_FILE = 13
        INEXISTENT_ITEM = 7
        INEXISTENT_TAG = 21
        INTERNAL_ERROR = -1
        JSON_TO_LUA_TABLE = 2029
        LUA_ALREADY_EXECUTED = 2032
        LUA_BAD_OUTPUT = 2033
        LUA_RETURNS_NO_STRING = 2035
        MAKE_DIRECTORY = 2008
        NETWORK_PROTOCOL = 9
        NOT_ACCEPTABLE = 34
        NOT_ENOUGH_MEMORY = 4
        NOT_IMPLEMENTED = 2
        NOT_LUA_PREDICATE = 2034
        NO_APPLICATION_ENTITY_FILTER = 2013
        NO_CFIND_HANDLER = 2010
        NO_CGET_HANDLER = 2044
        NO_CMOVE_HANDLER = 2011
        NO_CSTORE_HANDLER = 2012
        NO_PRESENTATION_CONTEXT = 2015
        NO_SOP_CLASS_OR_INSTANCE = 2014
        NO_STORAGE_COMMITMENT_HANDLER = 2043
        NO_WORKLIST_HANDLER = 2041
        NULL_POINTER = 35
        PARAMETER_OUT_OF_RANGE = 3
        PATH_TO_EXECUTABLE = 2007
        PLUGIN = 1
        READ_ONLY = 22
        REGULAR_FILE_EXPECTED = 2006
        REVISION = 43
        SHARED_LIBRARY = 25
        SQLITE_ALREADY_OPENED = 1001
        SQLITE_BIND_OUT_OF_RANGE = 1011
        SQLITE_CANNOT_OPEN = 1002
        SQLITE_CANNOT_RUN = 1009
        SQLITE_CANNOT_STEP = 1010
        SQLITE_COMMIT_WITHOUT_TRANSACTION = 1006
        SQLITE_EXECUTE = 1004
        SQLITE_FLUSH = 1008
        SQLITE_NOT_OPENED = 1000
        SQLITE_PREPARE_STATEMENT = 1012
        SQLITE_REGISTER_FUNCTION = 1007
        SQLITE_ROLLBACK_WITHOUT_TRANSACTION = 1005
        SQLITE_STATEMENT_ALREADY_USED = 1003
        SQLITE_TRANSACTION_ALREADY_STARTED = 1013
        SQLITE_TRANSACTION_BEGIN = 1015
        SQLITE_TRANSACTION_COMMIT = 1014
        SSL_DISABLED = 2039
        SSL_INITIALIZATION = 39
        STORAGE_AREA_ALREADY_REGISTERED = 2036
        STORAGE_AREA_PLUGIN = 32
        SUCCESS = 0
        SYSTEM_COMMAND = 10
        TIMEOUT = 16
        UNAUTHORIZED = 29
        UNKNOWN_DICOM_TAG = 27
        UNKNOWN_MODALITY = 2027
        UNKNOWN_PLUGIN_SERVICE = 26
        UNKNOWN_RESOURCE = 17
        UNSUPPORTED_MEDIA_TYPE = 3000
        URI_SYNTAX = 12


    class HttpMethod(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginHttpMethod"""
        DELETE = 4
        GET = 1
        POST = 2
        PUT = 3


    class IdentifierConstraint(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginIdentifierConstraint"""
        EQUAL = 1
        GREATER_OR_EQUAL = 3
        SMALLER_OR_EQUAL = 2
        WILDCARD = 4


    class ImageFormat(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginImageFormat"""
        DICOM = 2
        JPEG = 1
        PNG = 0


    class InstanceOrigin(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginInstanceOrigin"""
        DICOM_PROTOCOL = 2
        LUA = 5
        PLUGIN = 4
        REST_API = 3
        UNKNOWN = 1
        WEB_DAV = 6


    class JobStepStatus(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginJobStepStatus"""
        CONTINUE = 3
        FAILURE = 2
        SUCCESS = 1


    class JobStopReason(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginJobStopReason"""
        CANCELED = 4
        FAILURE = 3
        PAUSED = 2
        SUCCESS = 1


    class MetricsType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginMetricsType"""
        DEFAULT = 0
        TIMER = 1


    class PixelFormat(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginPixelFormat"""
        BGRA32 = 10
        FLOAT32 = 9
        GRAYSCALE16 = 2
        GRAYSCALE32 = 8
        GRAYSCALE64 = 11
        GRAYSCALE8 = 1
        RGB24 = 4
        RGB48 = 7
        RGBA32 = 5
        SIGNED_GRAYSCALE16 = 3
        UNKNOWN = 6


    class ReceivedInstanceAction(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginReceivedInstanceAction"""
        DISCARD = 3
        KEEP_AS_IS = 1
        MODIFY = 2


    class ResourceType(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginResourceType"""
        INSTANCE = 3
        NONE = 4
        PATIENT = 0
        SERIES = 2
        STUDY = 1


    class StorageCommitmentFailureReason(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginStorageCommitmentFailureReason"""
        CLASS_INSTANCE_CONFLICT = 5
        DUPLICATE_TRANSACTION_UID = 6
        NO_SUCH_OBJECT_INSTANCE = 2
        PROCESSING_FAILURE = 1
        REFERENCED_SOPCLASS_NOT_SUPPORTED = 4
        RESOURCE_LIMITATION = 3
        SUCCESS = 0


    class ValueRepresentation(Enum):
        """Generated from C enumeration OrthancPluginOrthancPluginValueRepresentation"""
        AE = 1
        AS = 2
        AT = 3
        CS = 4
        DA = 5
        DS = 6
        DT = 7
        FD = 8
        FL = 9
        IS = 10
        LO = 11
        LT = 12
        OB = 13
        OF = 14
        OW = 15
        PN = 16
        SH = 17
        SL = 18
        SQ = 19
        SS = 20
        ST = 21
        TM = 22
        UI = 23
        UL = 24
        UN = 25
        US = 26
        UT = 27


    def AutodetectMimeType(*args):
        """Generated from C function OrthancPluginAutodetectMimeType()"""
        pass


    def BufferCompression(memory_buffer: Any,
                          source: Any,
                          size: int,
                          compression: CompressionType,
                          uncompress: int) -> int:
        """Compress or decompress a buffer.

        This function compresses or decompresses a buffer, using the version of the zlib
        library that is used by the Orthanc core.
        
        Parameters
        ----------
        memory_buffer
            The target memory buffer. It must be freed with OrthancPluginFreeMemoryBuffer()
        source
            The source buffer.
        size
            The size in bytes of the source buffer.
        compression
            The compression algorithm.
        uncompress
            If set to "0", the buffer must be compressed.

        Returns
        -------
            0 if success, or the error code if failure. 
        """ 
        pass


    def CheckVersion() -> int:
        """Check the compatibility of the plugin wrt. the version of its hosting Orthanc.
        
        This function checks whether the version of the Orthanc server
        running this plugin, is above the version of the current Orthanc
        SDK header. This guarantees that the plugin is compatible with
        the hosting Orthanc (i.e. it will not call unavailable services).
        The result of this function should always be checked in the
        OrthancPluginInitialize() entry point of the plugin.
        
        Returns
        -------
            1 if and only if the versions are compatible. If the result is 0,
            the initialization of the plugin should fail.

        """
        pass


    def CheckVersionAdvanced(*args):
        """Generated from C function OrthancPluginCheckVersionAdvanced()"""
        pass


    def CompressJpegImage(*args):
        """Generated from C function OrthancPluginCompressJpegImage()"""
        pass


    def CompressPngImage(*args):
        """Generated from C function OrthancPluginCompressPngImage()"""
        pass


    def ComputeMd5(*args):
        """Generated from C function OrthancPluginComputeMd5()"""
        pass


    def ComputeSha1(*args):
        """Generated from C function OrthancPluginComputeSha1()"""
        pass


    def CreateDicom(*args):
        """None"""
        pass


    def CreateDicomInstance(*args):
        """Generated from C function OrthancPluginCreateDicomInstance()"""
        pass


    def CreateFindMatcher(*args):
        """Generated from C function OrthancPluginCreateFindMatcher()"""
        pass


    def CreateImage(*args):
        """Generated from C function OrthancPluginCreateImage()"""
        pass


    def CreateImageFromBuffer(*args):
        """None"""
        pass


    def CreateMemoryBuffer(*args):
        """Generated from C function OrthancPluginCreateMemoryBuffer()"""
        pass


    def DecodeDicomImage(*args):
        """Generated from C function OrthancPluginDecodeDicomImage()"""
        pass


    def DicomBufferToJson(*args):
        """Generated from C function OrthancPluginDicomBufferToJson()"""
        pass


    def DicomInstanceToJson(*args):
        """Generated from C function OrthancPluginDicomInstanceToJson()"""
        pass


    def ExtendOrthancExplorer(*args):
        """Generated from C function OrthancPluginExtendOrthancExplorer()"""
        pass


    def GenerateRestApiAuthorizationToken(*args):
        """Generated from C function OrthancPluginGenerateRestApiAuthorizationToken()"""
        pass


    def GenerateUuid(*args):
        """Generated from C function OrthancPluginGenerateUuid()"""
        pass


    def GetCommandLineArgument(*args):
        """Generated from C function OrthancPluginGetCommandLineArgument()"""
        pass


    def GetCommandLineArgumentsCount(*args):
        """Generated from C function OrthancPluginGetCommandLineArgumentsCount()"""
        pass


    def GetConfiguration(*args):
        """Generated from C function OrthancPluginGetConfiguration()"""
        pass


    def GetConfigurationPath(*args):
        """Generated from C function OrthancPluginGetConfigurationPath()"""
        pass


    def GetDicomForInstance(*args):
        """Generated from C function OrthancPluginGetDicomForInstance()"""
        pass


    def GetErrorDescription(*args):
        """Generated from C function OrthancPluginGetErrorDescription()"""
        pass


    def GetExpectedDatabaseVersion(*args):
        """Generated from C function OrthancPluginGetExpectedDatabaseVersion()"""
        pass


    def GetFontName(*args):
        """Generated from C function OrthancPluginGetFontName()"""
        pass


    def GetFontSize(*args):
        """Generated from C function OrthancPluginGetFontSize()"""
        pass


    def GetFontsCount(*args):
        """Generated from C function OrthancPluginGetFontsCount()"""
        pass


    def GetGlobalProperty(*args):
        """Generated from C function OrthancPluginGetGlobalProperty()"""
        pass


    def GetOrthancDirectory(*args):
        """Generated from C function OrthancPluginGetOrthancDirectory()"""
        pass


    def GetOrthancPath(*args):
        """Generated from C function OrthancPluginGetOrthancPath()"""
        pass


    def GetPeers(*args):
        """Generated from C function OrthancPluginGetPeers()"""
        pass


    def GetTagName(*args):
        """Generated from C function OrthancPluginGetTagName()"""
        pass


    def HttpDelete(*args):
        """Generated from C function OrthancPluginHttpDelete()"""
        pass


    def HttpGet(*args):
        """Generated from C function OrthancPluginHttpGet()"""
        pass


    def HttpPost(*args):
        """Generated from C function OrthancPluginHttpPost()"""
        pass


    def HttpPut(*args):
        """Generated from C function OrthancPluginHttpPut()"""
        pass


    def LogError(*args):
        """Generated from C function OrthancPluginLogError()"""
        pass


    def LogInfo(*args):
        """Generated from C function OrthancPluginLogInfo()"""
        pass


    def LogWarning(*args):
        """Generated from C function OrthancPluginLogWarning()"""
        pass


    def LookupDictionary(*args):
        """None"""
        pass


    def LookupInstance(*args):
        """Generated from C function OrthancPluginLookupInstance()"""
        pass


    def LookupPatient(*args):
        """Generated from C function OrthancPluginLookupPatient()"""
        pass


    def LookupSeries(*args):
        """Generated from C function OrthancPluginLookupSeries()"""
        pass


    def LookupStudy(*args):
        """Generated from C function OrthancPluginLookupStudy()"""
        pass


    def LookupStudyWithAccessionNumber(*args):
        """Generated from C function OrthancPluginLookupStudyWithAccessionNumber()"""
        pass


    def ReadFile(*args):
        """Generated from C function OrthancPluginReadFile()"""
        pass


    def RegisterDictionaryTag(*args):
        """Generated from C function OrthancPluginRegisterDictionaryTag()"""
        pass


    def RegisterErrorCode(*args):
        """Generated from C function OrthancPluginRegisterErrorCode()"""
        pass


    def RegisterFindCallback(*args):
        """None"""
        pass


    def RegisterIncomingCStoreInstanceFilter(*args):
        """None"""
        pass


    def RegisterIncomingHttpRequestFilter(*args):
        """None"""
        pass


    def RegisterMoveCallback(*args):
        """None"""
        pass


    def RegisterOnChangeCallback(*args):
        """None"""
        pass


    def RegisterOnStoredInstanceCallback(*args):
        """None"""
        pass


    def RegisterPrivateDictionaryTag(*args):
        """Generated from C function OrthancPluginRegisterPrivateDictionaryTag()"""
        pass


    def RegisterReceivedInstanceCallback(*args):
        """None"""
        pass


    def RegisterRestCallback(new_route: str, callback: Callable) -> None:
        """Register a REST callback.
        
        This function registers a REST callback against a regular
        expression for a URI. This function must be called during the
        initialization of the plugin, i.e. inside the
        OrthancPluginInitialize() public function.

        Parameters
        ----------
        new_route
            Regular expression for the URI. May contain groups.
        callback
            The callback function to handle the REST call.

        Examples
        --------
        ```python
        def on_rest(output, uri, **request):
            print(request)


        orthanc.RegisterRestCallback('/tata', on_rest)
        ```
        """
        pass


    def RegisterStorageArea(*args):
        """None"""
        pass


    def RegisterStorageCommitmentScpCallback(*args):
        """None"""
        pass


    def RegisterWorklistCallback(*args):
        """None"""
        pass


    def RestApiDelete(*args):
        """Generated from C function OrthancPluginRestApiDelete()"""
        pass


    def RestApiDeleteAfterPlugins(*args):
        """Generated from C function OrthancPluginRestApiDeleteAfterPlugins()"""
        pass


    def RestApiGet(*args):
        """Generated from C function OrthancPluginRestApiGet()"""
        pass


    def RestApiGetAfterPlugins(*args):
        """Generated from C function OrthancPluginRestApiGetAfterPlugins()"""
        pass


    def RestApiPost(uri: str, body: Any, *args, **kwargs):
        """Make a POST call to the built-in Orthanc REST API.
        
        Make a POST call to the built-in Orthanc REST API. The result to
        the query is stored into a newly allocated memory buffer.
        
        Parameters
        ----------
        uri
            The URI in the built-in Orthanc API.
        body
            The body of the POST request.
        *args
        **kwargs

        """
        pass


    def RestApiPostAfterPlugins(*args):
        """Generated from C function OrthancPluginRestApiPostAfterPlugins()"""
        pass


    def RestApiPut(*args):
        """Generated from C function OrthancPluginRestApiPut()"""
        pass


    def RestApiPutAfterPlugins(*args):
        """Generated from C function OrthancPluginRestApiPutAfterPlugins()"""
        pass


    def SetDescription(*args):
        """Generated from C function OrthancPluginSetDescription()"""
        pass


    def SetGlobalProperty(*args):
        """Generated from C function OrthancPluginSetGlobalProperty()"""
        pass


    def SetMetricsValue(*args):
        """Generated from C function OrthancPluginSetMetricsValue()"""
        pass


    def SetRootUri(*args):
        """Generated from C function OrthancPluginSetRootUri()"""
        pass


    def TranscodeDicomInstance(*args):
        """Generated from C function OrthancPluginTranscodeDicomInstance()"""
        pass


    def UncompressImage(*args):
        """Generated from C function OrthancPluginUncompressImage()"""
        pass


    def WriteFile(*args):
        """Generated from C function OrthancPluginWriteFile()"""
        pass


    class DicomInstance:
        """Generated from Orthanc C class: OrthancPluginDicomInstance"""

        def GetInstanceAdvancedJson(self, *args):
            """Generated from C function OrthancPluginGetInstanceAdvancedJson()"""
            pass

        def GetInstanceData(self, *args):
            """Generated from C function OrthancPluginGetInstanceData()"""
            pass

        def GetInstanceDecodedFrame(self, *args):
            """Generated from C function OrthancPluginGetInstanceDecodedFrame()"""
            pass

        def GetInstanceFramesCount(self, *args):
            """Generated from C function OrthancPluginGetInstanceFramesCount()"""
            pass

        def GetInstanceJson(self, *args):
            """Generated from C function OrthancPluginGetInstanceJson()"""
            pass

        def GetInstanceMetadata(self, *args):
            """Generated from C function OrthancPluginGetInstanceMetadata()"""
            pass

        def GetInstanceOrigin(self, *args):
            """Generated from C function OrthancPluginGetInstanceOrigin()"""
            pass

        def GetInstanceRawFrame(self, *args):
            """Generated from C function OrthancPluginGetInstanceRawFrame()"""
            pass

        def GetInstanceRemoteAet(self, *args):
            """Generated from C function OrthancPluginGetInstanceRemoteAet()"""
            pass

        def GetInstanceSimplifiedJson(self, *args):
            """Generated from C function OrthancPluginGetInstanceSimplifiedJson()"""
            pass

        def GetInstanceSize(self, *args):
            """Generated from C function OrthancPluginGetInstanceSize()"""
            pass

        def GetInstanceTransferSyntaxUid(self, *args):
            """Generated from C function OrthancPluginGetInstanceTransferSyntaxUid()"""
            pass

        def HasInstanceMetadata(self, *args):
            """Generated from C function OrthancPluginHasInstanceMetadata()"""
            pass

        def HasInstancePixelData(self, *args):
            """Generated from C function OrthancPluginHasInstancePixelData()"""
            pass

        def SerializeDicomInstance(self, *args):
            """Generated from C function OrthancPluginSerializeDicomInstance()"""
            pass


    class FindAnswers:
        """Generated from Orthanc C class: OrthancPluginFindAnswers"""

        def FindAddAnswer(self, *args):
            """Generated from C function OrthancPluginFindAddAnswer()"""
            pass

        def FindMarkIncomplete(self, *args):
            """Generated from C function OrthancPluginFindMarkIncomplete()"""
            pass


    class FindMatcher:
        """Generated from Orthanc C class: OrthancPluginFindMatcher"""

        def FindMatcherIsMatch(self, *args):
            """Generated from C function OrthancPluginFindMatcherIsMatch()"""
            pass


    class FindQuery:
        """Generated from Orthanc C class: OrthancPluginFindQuery"""

        def GetFindQuerySize(self, *args):
            """Generated from C function OrthancPluginGetFindQuerySize()"""
            pass

        def GetFindQueryTagElement(self, *args):
            """Generated from C function OrthancPluginGetFindQueryTag()"""
            pass

        def GetFindQueryTagGroup(self, *args):
            """Generated from C function OrthancPluginGetFindQueryTag()"""
            pass

        def GetFindQueryTagName(self, *args):
            """Generated from C function OrthancPluginGetFindQueryTagName()"""
            pass

        def GetFindQueryValue(self, *args):
            """Generated from C function OrthancPluginGetFindQueryValue()"""
            pass


    class Image:
        """Generated from Orthanc C class: OrthancPluginImage"""

        def ConvertPixelFormat(self, *args):
            """Generated from C function OrthancPluginConvertPixelFormat()"""
            pass

        def DrawText(self, *args):
            """Generated from C function OrthancPluginDrawText()"""
            pass

        def GetImageBuffer(self, *args):
            """Generated from C function OrthancPluginGetImageBuffer()"""
            pass

        def GetImageHeight(self, *args):
            """Generated from C function OrthancPluginGetImageHeight()"""
            pass

        def GetImagePitch(self, *args):
            """Generated from C function OrthancPluginGetImagePitch()"""
            pass

        def GetImagePixelFormat(self, *args):
            """Generated from C function OrthancPluginGetImagePixelFormat()"""
            pass

        def GetImageWidth(self, *args):
            """Generated from C function OrthancPluginGetImageWidth()"""
            pass


    class Job:
        """Generated from Orthanc C class: OrthancPluginJob"""

        def SubmitJob(self, *args):
            """Generated from C function OrthancPluginSubmitJob()"""
            pass


    class OrthancException:
        """Common base class for all non-exit exceptions."""

        def with_traceback(self, *args):
            """Exception.with_traceback(tb) -- set self.__traceback__ to tb and return self."""
            pass


    class Peers:
        """Generated from Orthanc C class: OrthancPluginPeers"""

        def GetPeerName(self, *args):
            """Generated from C function OrthancPluginGetPeerName()"""
            pass

        def GetPeerUrl(self, *args):
            """Generated from C function OrthancPluginGetPeerUrl()"""
            pass

        def GetPeerUserProperty(self, *args):
            """Generated from C function OrthancPluginGetPeerUserProperty()"""
            pass

        def GetPeersCount(self, *args):
            """Generated from C function OrthancPluginGetPeersCount()"""
            pass


    class RestOutput:
        """Generated from Orthanc C class: OrthancPluginRestOutput"""

        def AnswerBuffer(self, *args):
            """Generated from C function OrthancPluginAnswerBuffer()"""
            pass

        def CompressAndAnswerJpegImage(self, *args):
            """Generated from C function OrthancPluginCompressAndAnswerJpegImage()"""
            pass

        def CompressAndAnswerPngImage(self, *args):
            """Generated from C function OrthancPluginCompressAndAnswerPngImage()"""
            pass

        def Redirect(self, *args):
            """Generated from C function OrthancPluginRedirect()"""
            pass

        def SendHttpStatus(self, *args):
            """Generated from C function OrthancPluginSendHttpStatus()"""
            pass

        def SendHttpStatusCode(self, *args):
            """Generated from C function OrthancPluginSendHttpStatusCode()"""
            pass

        def SendMethodNotAllowed(self, *args):
            """Generated from C function OrthancPluginSendMethodNotAllowed()"""
            pass

        def SendMultipartItem(self, *args):
            """Generated from C function OrthancPluginSendMultipartItem()"""
            pass

        def SendUnauthorized(self, *args):
            """Generated from C function OrthancPluginSendUnauthorized()"""
            pass

        def SetCookie(self, *args):
            """Generated from C function OrthancPluginSetCookie()"""
            pass

        def SetHttpErrorDetails(self, *args):
            """Generated from C function OrthancPluginSetHttpErrorDetails()"""
            pass

        def SetHttpHeader(self, *args):
            """Generated from C function OrthancPluginSetHttpHeader()"""
            pass

        def StartMultipartAnswer(self, *args):
            """Generated from C function OrthancPluginStartMultipartAnswer()"""
            pass


    class ServerChunkedRequestReader:
        """Generated from Orthanc C class: OrthancPluginServerChunkedRequestReader"""


    class StorageArea:
        """Generated from Orthanc C class: OrthancPluginStorageArea"""

        def ReconstructMainDicomTags(self, *args):
            """Generated from C function OrthancPluginReconstructMainDicomTags()"""
            pass

        def StorageAreaCreate(self, *args):
            """Generated from C function OrthancPluginStorageAreaCreate()"""
            pass

        def StorageAreaRead(self, *args):
            """Generated from C function OrthancPluginStorageAreaRead()"""
            pass

        def StorageAreaRemove(self, *args):
            """Generated from C function OrthancPluginStorageAreaRemove()"""
            pass


    class WorklistAnswers:
        """Generated from Orthanc C class: OrthancPluginWorklistAnswers"""

        def WorklistAddAnswer(self, *args):
            """Generated from C function OrthancPluginWorklistAddAnswer()"""
            pass

        def WorklistMarkIncomplete(self, *args):
            """Generated from C function OrthancPluginWorklistMarkIncomplete()"""
            pass


    class WorklistQuery:
        """Generated from Orthanc C class: OrthancPluginWorklistQuery"""

        def WorklistGetDicomQuery(self, *args):
            """Generated from C function OrthancPluginWorklistGetDicomQuery()"""
            pass

        def WorklistIsMatch(self, *args):
            """Generated from C function OrthancPluginWorklistIsMatch()"""
            pass


    class __loader__:
        """Meta path import for built-in modules."""
