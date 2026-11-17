import re
from typing import Dict, Iterable, Tuple

import simple_openapi_client
from simple_openapi_client.maker import _make_function_name

ORTHANC_API_URL = 'https://orthanc.uclouvain.be/api/orthanc-openapi.json'

# Return annotation written by the simple_openapi_client templates (after the httpx -> httpx2 substitution)
GENERIC_RETURN_TYPE = 'Union[Dict, List, str, bytes, int, httpx2.Response]'

# Routes whose documented response content type does not match what Orthanc sends (checked against Orthanc)
RETURN_TYPE_CORRECTIONS = {
    # Documented as "text/plain", but Orthanc sends a binary NumPy (.npy) file
    'get_instances_id_numpy': 'bytes',
    'get_instances_id_frames_frame_numpy': 'bytes',
    'get_series_id_numpy': 'bytes',
    # Documented as "application/octet-stream", but Orthanc answers JSON when the path points to a sequence
    'get_instances_id_content_path': 'Any',
}


def generate_client(path: str, async_mode: bool = False):
    config = simple_openapi_client.Config(client_name='AsyncOrthanc' if async_mode else 'Orthanc')

    document = simple_openapi_client.parse_openapi(ORTHANC_API_URL)
    document = _apply_corrections_to_documents(document)
    client_str = simple_openapi_client.make_client(document, config, async_mode=async_mode, use_black=True)
    # simple_openapi_client templates are written for httpx, pyorthanc uses its maintained fork httpx2
    client_str = re.sub(r'\bhttpx\b', 'httpx2', client_str)
    client_str = annotate_return_types(client_str, make_return_types(document))

    with open(path, 'w') as file:
        file.write(client_str)


def make_return_types(document) -> Dict[str, str]:
    """Map each generated method name to the return annotation deduced from its response content types.

    The mapping mirrors how `Orthanc._get()` (and friends) deserialize a response at runtime:
    "application/json" -> `response.json()`, "text/plain" -> `response.text`, anything else -> `response.content`.
    """
    return_types = {}

    for route, path in document.paths.items():
        if path.operations is None:
            continue

        for operation_name, operation in path.operations.items():
            function_name = _make_function_name(route.replace('id', 'id_'), operation_name)
            return_types[function_name] = _return_type_from_content_types(_success_content_types(operation))

    for function_name, return_type in RETURN_TYPE_CORRECTIONS.items():
        if function_name not in return_types:
            raise ValueError(f'Return type correction for an unknown method: "{function_name}".')
        return_types[function_name] = return_type

    return return_types


def _success_content_types(operation) -> Iterable[str]:
    content_types = set()

    for status_code, response in operation.responses.items():
        if status_code.startswith('2') and response.content is not None:
            content_types |= set(response.content.keys())

    return content_types


def _return_type_from_content_types(content_types: Iterable[str]) -> str:
    kinds = set()

    for content_type in content_types:
        if 'application/json' in content_type:  # Same test as in Orthanc._get()
            kinds.add('json')
        elif 'text/plain' in content_type:
            kinds.add('text')
        else:
            kinds.add('bytes')

    if kinds == {'text'}:
        return 'str'
    if kinds == {'bytes'}:
        return 'bytes'

    # JSON responses (dict, list, str, int, ...), routes documenting several kinds
    # of responses and routes without documented content are left as `Any`.
    return 'Any'


def annotate_return_types(client_str: str, return_types: Dict[str, str]) -> str:
    """Replace the generic return annotation of the generated methods with the deduced ones.

    The private request helpers (`_get`, `_post`, ...) are annotated with `Any`.
    """
    for function_name, return_type in [*_request_helpers(), *return_types.items()]:
        pattern = re.compile(
            rf'(\n    (?:async )?def {function_name}\(.*?\) -> ){re.escape(GENERIC_RETURN_TYPE)}'
            rf'(:.*?Returns\n\s*-------\n\s*){re.escape(GENERIC_RETURN_TYPE)}',
            flags=re.DOTALL,
        )
        client_str, count = pattern.subn(rf'\g<1>{return_type}\g<2>{return_type}', client_str)

        if count != 1:
            raise ValueError(f'Expected to annotate exactly one "{function_name}" method, found {count}.')

    if GENERIC_RETURN_TYPE in client_str:
        raise ValueError('Some methods still have the generic return annotation.')

    return client_str


def _request_helpers() -> Iterable[Tuple[str, str]]:
    return [(f'_{method}', 'Any') for method in ('get', 'delete', 'post', 'put')]


def _apply_corrections_to_documents(document):
    """Correcting Orthanc OpenAPI specs"""
    to_change = []

    for route, path in document.paths.items():
        if path.operations is not None:
            for operation_name, operation in path.operations.items():
                if operation.parameters is None:
                    continue

                for param in operation.parameters:
                    if param.name == '...':
                        param.name = 'tags_path'

                        to_change.append({
                            'old_route': route,
                            'new_route': route + '/{tags_path}',
                        })

    for change in to_change:
        document.paths[change['new_route']] = document.paths.pop(change['old_route'])

    return document


if __name__ == '__main__':
    generate_client('./pyorthanc/client.py', async_mode=False)
    generate_client('./pyorthanc/async_client.py', async_mode=True)
