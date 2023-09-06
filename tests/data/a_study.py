import os
from datetime import datetime

import pydicom

IDENTIFIER = '118bc493-b3b3172a-082119bd-f6802ec3-81695613'
PARENT_PATIENT_IDENTIFIER = 'e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8'
PATIENT_MAIN_INFORMATION = {
    'PatientBirthDate': '19410901',
    'PatientID': '03HDQ000',
    'PatientName': 'MR-R',
    'PatientSex': 'M',
    'OtherPatientIDs': 'other-id-1\\other-id-2'
}
DATE = datetime(year=2010, month=2, day=23)
REFERRING_PHYSICIAN_NAME = ''
ID = ''
SERIES = [
    'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06',
    '60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b',
    'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96',
]
UID = '1.2.840.113619.2.55.3.671782272.419.1266452812.128'
INFORMATION = {
    'ID': IDENTIFIER,
    'IsStable': False,
    'Labels': [],
    'LastUpdate': '20190913T185658',
    'MainDicomTags': {
        'AccessionNumber': '',
        'ReferringPhysicianName': '',
        'StudyDate': '20100223',
        'StudyID': ID,
        'StudyInstanceUID': UID,
        'StudyTime': '',
    },
    'ParentPatient': PARENT_PATIENT_IDENTIFIER,
    'PatientMainDicomTags': PATIENT_MAIN_INFORMATION,
    'Series': SERIES,
    'Type': 'Study'
}
ZIP_FILE_PATH = './tests/data/A_STUDY_DATA.zip'
INSTANCES = [
    {
        'FileSize': 61742,
        'FileUuid': '6b20abc4-67af-4d2b-b537-b0ee3b35b4df',
        'ID': 'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599',
        'IndexInSeries': None,
        'Labels': [],
        'MainDicomTags': {
            'InstanceCreationDate': '20100301',
            'InstanceCreationTime': '170155',
            'SOPInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170155.103167'
        },
        'ParentSeries': '60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b',
        'Type': 'Instance'
    },
    {
        'FileSize': 10373100,
        'FileUuid': '89b19e2c-9bfb-4751-a539-d54ac9a3d912',
        'ID': '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220',
        'IndexInSeries': None,
        'Labels': [],
        'MainDicomTags': {
            'InstanceCreationDate': '20100301',
            'InstanceCreationTime': '170155',
            'SOPInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170148.768438'
        },
        'ParentSeries': 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96',
        'Type': 'Instance'
    },
    {
        'FileSize': 1506520,
        'FileUuid': '0aa5b638-7531-4863-a23f-7695aa1577ef',
        'ID': '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9',
        'IndexInSeries': 1,
        'Labels': [],
        'MainDicomTags': {
            'ImageOrientationPatient': '1\\0\\0\\0\\1\\0',
            'ImagePositionPatient': '-223.9880065918\\-158.08148193359\\-117.78499603271',
            'InstanceCreationDate': '20100301',
            'InstanceCreationTime': '170155',
            'InstanceNumber': '1',
            'NumberOfFrames': '75',
            'SOPInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170155.668389'},
        'ParentSeries': 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06',
        'Type': 'Instance'
    }
]

STUDY_INSTANCE_UIDS = []
for path in [f'./tests/data/orthanc_1_test_data/{i}' for i in os.listdir('tests/data/orthanc_1_test_data')]:
    _ds = pydicom.dcmread(path)
    STUDY_INSTANCE_UIDS.append(_ds.StudyInstanceUID)
