import simple_openapi_client

ORTHANC_API_URL = 'https://api.orthanc-server.com/orthanc-openapi.json'


def generate_client(path: str):
    config = simple_openapi_client.Config(client_name='Orthanc')

    document = simple_openapi_client.parse_openapi(ORTHANC_API_URL)
    document = _apply_corrections_to_documents(document)
    client_str = simple_openapi_client.make_client(document, config)

    with open(path, 'w') as file:
        file.write(client_str)


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
    generate_client('../pyorthanc/client.py')
