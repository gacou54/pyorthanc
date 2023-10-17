# Orthanc SDK

The `orthanc_sdk` is useful when developing with the Orthanc's Python Plugin, 
it exposes `orthanc` module when available (i.e. used as an Orthanc script), 
or expose the functions/classes signatures when not for linting and autocomplete.

Use it the same way you would use the Python Plugin:

```python
from pyorthanc import orthanc_sdk

def on_get(output: orthanc_sdk.RestOutput, *_, **__):
    output.AnswerBuffer('ok', 'text/plain')

orthanc_sdk.RegisterRestCallback('/test', on_get)
```


## How it works
When developing importing the Orthanc Python Plugin with `import orthanc` will raise a `ModuleNotFoundError`.
This where the `orthanc_sdk` submodule is interesting. When `orthanc` is available, it uses it.
When not, `orthanc_sdk` expose mock functions/classes of everything available from `orthanc`, however, these functions/classes does nothing.

```python
try:
    from orthanc import *

except ModuleNotFoundError:
    """Orthanc SDK methods wrapped in python (plugin version 4.0)"""
    ...
```


## Reference

::: pyorthanc.orthanc_sdk
    options:
        members: true
    :docstring:
    :members:
