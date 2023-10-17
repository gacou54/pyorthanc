from enum import Enum


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
