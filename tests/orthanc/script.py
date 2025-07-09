import json

from pyorthanc import find_series, get_internal_client, orthanc_sdk


def on_get(output: orthanc_sdk.RestOutput, *_, **__):
    output.AnswerBuffer('ok', 'text/plain')


def on_get_internal_client(output: orthanc_sdk.RestOutput, *_, **__):
    """This function returns all modalities in Orthanc."""
    client = get_internal_client()

    series = find_series(client)
    modalities_in_orthanc = set([s.modality for s in series])

    output.AnswerBuffer(
        json.dumps({'modalities': list(modalities_in_orthanc)}),
        'application/json'
    )


orthanc_sdk.RegisterRestCallback('/test', on_get)
orthanc_sdk.RegisterRestCallback('/test-internal-client', on_get_internal_client)
