from pyorthanc import orthanc_sdk


def on_get(output: orthanc_sdk.RestOutput, *_, **__):
    output.AnswerBuffer('ok', 'text/plain')


orthanc_sdk.RegisterRestCallback('/test', on_get)
