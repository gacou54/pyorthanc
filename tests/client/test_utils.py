def test_system(client):
    result = client.get_system()

    assert 'Version' in result
    assert 'ApiVersion' in result
    assert 'DicomAet' in result
    assert 'DicomPort' in result
    assert 'MainDicomTags' in result
    assert 'Capabilities' in result


def test_changes(client):
    result = client.get_changes()

    assert 'Changes' in result
    assert 'Done' in result
    assert 'Last' in result

    result = client.get_changes(params={'type': 'StableStudy'})  # Example of type to filter on

    assert 'Changes' in result
    assert 'Done' in result
    assert 'Last' in result


def test_find(client_with_data_and_labels):
    result = client_with_data_and_labels.post_tools_find(json={
        'Level': 'Patient',
        'Query': {'PatientID': '*'}
    })
    assert result == ['e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8']

    result = client_with_data_and_labels.post_tools_find(json={
        'Level': 'Patient',
        'Labels': ['UNKNOWN_LABEL'],
        'Query': {'PatientID': '*'}
    })
    assert result == []


def test_count_resources(client_with_data_and_labels):
    result = client_with_data_and_labels.post_tools_count_resources(json={
        'Level': 'Patient',
        'Query': {'PatientID': '*'}
    })
    assert result['Count'] == 1

    result = client_with_data_and_labels.post_tools_count_resources(json={
        'Level': 'Patient',
        'Labels': ['UNKNOWN_LABEL'],
        'Query': {'PatientID': '*'}
    })
    assert result['Count'] == 0
