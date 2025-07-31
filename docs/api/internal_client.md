# Internal Client

The `orthanc_sdk` is useful when developing with the Orthanc's Python Plugin.
However, it is sometimes useful to have an instance of `pyorthanc.Orthanc` inside a Python script in Orthanc
to use the Orthanc REST API functionalities. This is where `pyorthanc.get_internal_client()` is helpful.

In a Python script, you can use `pyorthanc.get_internal_client()` to get an instance of `pyorthanc.Orthanc`
that can be used to call Orthanc's REST API.

```python
import json
from pyorthanc import orthanc_sdk, get_internal_client, find_studies


def get_study_descriptions(output: orthanc_sdk.RestOutput, *_, **__):
    # client is a pyorthanc.Orthanc instance
    client = get_internal_client()

    # You can use all functionalities of the pyorthanc.Orthanc now.
    # For example, we can retrieve all the study descriptions
    studies = find_studies(client)
    descriptions = [study.description for study in studies]

    output.AnswerBuffer(
        json.dumps({'descriptions': descriptions}),
        'application/json'
    )


orthanc_sdk.RegisterRestCallback('/all-study-descriptions', get_study_descriptions)
```

## How it works

`get_internal_client()` retrieve the correct URL, port and Token to allow Orthanc to call itself through the REST API.

## Reference

::: pyorthanc._internal_client
options:
members: true
:docstring:
:members:
