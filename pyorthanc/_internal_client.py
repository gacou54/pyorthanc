import json

from . import Orthanc
from .errors import NotInInternalEnvironmentError


def get_internal_client() -> Orthanc:
    """
    Returns an Orthanc client that can be used inside the Orthanc server in python scripts.

    Examples
    -------
    This example shows how to use the Orthanc REST API inside an Orthanc Python Script.
    >>> from pyorthanc import get_internal_client, find_series, orthanc_sdk
    >>> def get_modalities_in_orthanc(output: orthanc_sdk.RestOutput, *_, **__):
    ...     '''This function returns all modalities in Orthanc.'''
    ...     client = get_internal_client()
    ...
    ...     series = find_series(client)
    ...     modalities_in_orthanc = set([s.modality for s in series])
    ...
    ...     output.AnswerBuffer(
    ...         json.dumps({'modalities': list(modalities_in_orthanc)}),
    ...         'application/json'
    ...     )
    ...
    ... orthanc_sdk.RegisterRestCallback('/get-modalities-in-orthanc', get_modalities_in_orthanc)
    """
    from pyorthanc import orthanc_sdk

    config = orthanc_sdk.GetConfiguration()

    if not config:
        raise NotInInternalEnvironmentError(
            'This function is only available inside Orthanc server. '
            'Use `pyorthanc.get_internal_client()` inside a Orthanc Python Script. '
            'An `pyorthanc.Orthanc()` instance should be defined when using the '
            'Orthanc REST API outside of an Orthanc Oython Python Script.'
        )

    port = json.loads(config).get('HttpPort', 8042)
    url = f'http://localhost:{port}'

    client = Orthanc(url=url)

    token = orthanc_sdk.GenerateRestApiAuthorizationToken()
    client.headers['Authorization'] = token

    return client
