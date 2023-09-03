import time
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from . import util
from .client import Orthanc


class State(Enum):
    failure = 'Failure'
    paused = 'Paused'
    pending = 'Pending'
    retry = 'Retry'
    running = 'Running'
    success = 'Success'


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


class Job:

    def __init__(self, id_: str, client: Orthanc):
        self.id_ = id_
        self.client = client

    @property
    def state(self) -> State:
        state = self.get_information()['State']

        return State(state)

    @property
    def content(self) -> Dict:
        return self.get_information()['Content']

    @property
    def type(self) -> str:
        return self.get_information()['Type']

    @property
    def creation_time(self) -> datetime:
        creation_time = self.get_information()['CreationTime'].split('T')
        date = creation_time[0]
        time = creation_time[1]

        return util.make_datetime_from_dicom_date(date, time)

    @property
    def effective_runtime(self) -> float:
        runtime = self.get_information()['EffectiveRuntime']

        return float(runtime)

    @property
    def priority(self) -> int:
        return int(self.get_information()['Priority'])

    @property
    def progress(self) -> int:
        return int(self.get_information()['Progress'])

    @property
    def error(self) -> ErrorCode:
        info = self.get_information()

        return ErrorCode(info['ErrorCode'])

    @property
    def error_details(self) -> Optional[str]:
        info = self.get_information()

        if 'ErrorDetails' in info:
            return info['ErrorDetails']

        return None

    @property
    def timestamp(self) -> datetime:
        timestamp = self.get_information()['Timestamp'].split('T')
        date = timestamp[0]
        time = timestamp[1]

        return util.make_datetime_from_dicom_date(date, time)

    @property
    def completion_time(self) -> Optional[datetime]:
        info = self.get_information()

        if 'CompletionTime' not in info:
            return

        completion_time = self.get_information()['CompletionTime'].split('T')
        date = completion_time[0]
        time = completion_time[1]

        return util.make_datetime_from_dicom_date(date, time)

    def wait_until_completion(self, time_interval: int = 2) -> None:
        """Stop execution until job is not Pending/Running

        Parameters
        ----------
        time_interval
            Time interval to check the job status, default 2s.
        """
        while self.state in [State.pending, State.running]:
            time.sleep(time_interval)

    def get_information(self):
        return self.client.get_jobs_id(self.id_)
