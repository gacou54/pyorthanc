IDENTIFIER = 'e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8'
ID = '03HDQ000'
NAME = 'MR-R'
SEX = 'M'
INFORMATION = {
    'ID': IDENTIFIER,
    'IsStable': False,
    'LastUpdate': 'THIS_IS_VARIABLE',
    'Labels': [],
    'MainDicomTags': {
        'PatientBirthDate': '19410901',
        'PatientID': ID,
        'PatientName': NAME,
        'PatientSex': SEX,
        'OtherPatientIDs': 'other-id-1\\other-id-2'
    },
    'Studies': ['118bc493-b3b3172a-082119bd-f6802ec3-81695613'],
    'Type': 'Patient'
}

LIST_OF_INSTANCE_IDENTIFIERS_OF_A_PATIENT = [
    'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599',
    '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220',
    '22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9'
]

ZIP_FILE_PATH = './tests/data/A_PATIENT_DATA.zip'
MODULE = {
    '0010,0010': {'Name': 'PatientName', 'Type': 'String', 'Value': 'MR-R'},
    '0010,0020': {'Name': 'PatientID', 'Type': 'String', 'Value': '03HDQ000'},
    '0010,0030': {'Name': 'PatientBirthDate', 'Type': 'String', 'Value': '19410901'},
    '0010,0040': {'Name': 'PatientSex', 'Type': 'String', 'Value': 'M'},
    '0010,1000': {'Name': 'OtherPatientIDs', 'Type': 'String', 'Value': 'other-id-1\\other-id-2'},
}
MODULE_IN_SIMPLIFIED_VERSION = {
    'PatientBirthDate': '19410901',
    'PatientID': '03HDQ000',
    'PatientName': 'MR-R',
    'PatientSex': 'M',
    'OtherPatientIDs': 'other-id-1\\other-id-2',
}
MODULE_IN_SHORTER_VERSION = {
    '0010,0010': 'MR-R',
    '0010,0020': '03HDQ000',
    '0010,0030': '19410901',
    '0010,0040': 'M',
    '0010,1000': 'other-id-1\\other-id-2'
}
SHARED_TAGS = {
    '0008,0012': {'Name': 'InstanceCreationDate', 'Type': 'String', 'Value': '20100301'},
    '0008,0013': {'Name': 'InstanceCreationTime', 'Type': 'String', 'Value': '170155'},
    '0008,0020': {'Name': 'StudyDate', 'Type': 'String', 'Value': '20100223'},
    '0008,0030': {'Name': 'StudyTime', 'Type': 'String', 'Value': ''},
    '0008,0050': {'Name': 'AccessionNumber', 'Type': 'String', 'Value': ''},
    '0008,0070': {'Name': 'Manufacturer', 'Type': 'String', 'Value': 'ADAC'},
    '0008,0090': {'Name': 'ReferringPhysicianName', 'Type': 'String', 'Value': ''},
    '0008,1010': {'Name': 'StationName', 'Type': 'String', 'Value': 'pinnc-2'},
    '0008,1090': {'Name': 'ManufacturerModelName', 'Type': 'String', 'Value': 'Pinnacle3'},
    '0010,0010': {'Name': 'PatientName', 'Type': 'String', 'Value': 'MR-R'},
    '0010,0020': {'Name': 'PatientID', 'Type': 'String', 'Value': '03HDQ000'},
    '0010,0030': {'Name': 'PatientBirthDate', 'Type': 'String', 'Value': '19410901'},
    '0010,0040': {'Name': 'PatientSex', 'Type': 'String', 'Value': 'M'},
    '0010,1000': {'Name': 'OtherPatientIDs', 'Type': 'String', 'Value': 'other-id-1\\other-id-2'},
    '0018,1020': {'Name': 'SoftwareVersions', 'Type': 'String', 'Value': 'OCP x.x'},
    '0020,000d': {'Name': 'StudyInstanceUID', 'Type': 'String', 'Value': '1.2.840.113619.2.55.3.671782272.419.1266452812.128'},
    '0020,0010': {'Name': 'StudyID', 'Type': 'String', 'Value': ''},
    '0020,0011': {'Name': 'SeriesNumber', 'Type': 'String', 'Value': ''}
}
SHARED_TAGS_IN_SIMPLIFIED_VERSION = {
    'AccessionNumber': '',
    'InstanceCreationDate': '20100301',
    'InstanceCreationTime': '170155',
    'Manufacturer': 'ADAC',
    'ManufacturerModelName': 'Pinnacle3',
    'PatientBirthDate': '19410901',
    'PatientID': '03HDQ000',
    'PatientName': 'MR-R',
    'PatientSex': 'M',
    'OtherPatientIDs': 'other-id-1\\other-id-2',
    'ReferringPhysicianName': '',
    'SeriesNumber': '',
    'SoftwareVersions': 'OCP x.x',
    'StationName': 'pinnc-2',
    'StudyDate': '20100223',
    'StudyID': '',
    'StudyInstanceUID': '1.2.840.113619.2.55.3.671782272.419.1266452812.128',
    'StudyTime': ''
}
SHARED_TAGS_IN_SHORTER_VERSION = {
    '0008,0012': '20100301',
    '0008,0013': '170155',
    '0008,0020': '20100223',
    '0008,0030': '',
    '0008,0050': '',
    '0008,0070': 'ADAC',
    '0008,0090': '',
    '0008,1010': 'pinnc-2',
    '0008,1090': 'Pinnacle3',
    '0010,0010': 'MR-R',
    '0010,0020': '03HDQ000',
    '0010,0030': '19410901',
    '0010,0040': 'M',
    '0010,1000': 'other-id-1\\other-id-2',
    '0018,1020': 'OCP x.x',
    '0020,000d': '1.2.840.113619.2.55.3.671782272.419.1266452812.128',
    '0020,0010': '',
    '0020,0011': ''
}
STATISTICS = {
    'CountInstances': 3,
    'CountSeries': 3,
    'CountStudies': 1,
    'DicomDiskSize': '11941362',
    'DicomDiskSizeMB': 11,
    'DicomUncompressedSize': '11941362',
    'DicomUncompressedSizeMB': 11,
    'DiskSize': '12937775',
    'DiskSizeMB': 12,
    'UncompressedSize': '12937775',
    'UncompressedSizeMB': 12
}
SERIES = [{'ExpectedNumberOfInstances': None, 'ID': 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06', 'Instances': ['22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9'], 'IsStable': False, 'Labels': [], 'LastUpdate': '20190810T020641', 'MainDicomTags': {'ImageOrientationPatient': '1\\0\\0\\0\\1\\0', 'Manufacturer': 'ADAC', 'Modality': 'RTDOSE', 'SeriesInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170148.767969', 'SeriesNumber': '', 'StationName': 'pinnc-2'}, 'ParentStudy': '118bc493-b3b3172a-082119bd-f6802ec3-81695613', 'Status': 'Unknown', 'Type': 'Series'}, {'ExpectedNumberOfInstances': None, 'ID': 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96', 'Instances': ['348befe7-5be5ff53-70120381-3baa0cc2-e4e04220'], 'IsStable': False, 'Labels': [], 'LastUpdate': '20190810T020642', 'MainDicomTags': {'Manufacturer': 'ADAC', 'Modality': 'RTSTRUCT', 'SeriesDescription': 'Pinnacle POI', 'SeriesInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170148.767959', 'SeriesNumber': '', 'StationName': 'pinnc-2'}, 'ParentStudy': '118bc493-b3b3172a-082119bd-f6802ec3-81695613', 'Status': 'Unknown', 'Type': 'Series'}, {'ExpectedNumberOfInstances': None, 'ID': '60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b', 'Instances': ['da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599'], 'IsStable': False, 'Labels': [], 'LastUpdate': '20190810T020642', 'MainDicomTags': {'Manufacturer': 'ADAC', 'Modality': 'RTPLAN', 'OperatorsName': '', 'SeriesInstanceUID': '2.16.840.1.113669.2.931128.981194414.20100301170148.767977', 'SeriesNumber': '', 'StationName': 'pinnc-2'}, 'ParentStudy': '118bc493-b3b3172a-082119bd-f6802ec3-81695613', 'Status': 'Unknown', 'Type': 'Series'}]
STUDIES = [{'ID': '118bc493-b3b3172a-082119bd-f6802ec3-81695613', 'IsStable': False, 'Labels': [], 'LastUpdate': '20190819T193722', 'MainDicomTags': {'AccessionNumber': '', 'ReferringPhysicianName': '', 'StudyDate': '20100223', 'StudyID': '', 'StudyInstanceUID': '1.2.840.113619.2.55.3.671782272.419.1266452812.128', 'StudyTime': ''}, 'ParentPatient': 'e34c28ce-981b0e5c-2a481559-cf0d5fbe-053335f8', 'PatientMainDicomTags': {'OtherPatientIDs': 'other-id-1\\other-id-2', 'PatientBirthDate': '19410901', 'PatientID': '03HDQ000', 'PatientName': 'MR-R', 'PatientSex': 'M'}, 'Series': ['c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06', 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96', '60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b'], 'Type': 'Study'}]
