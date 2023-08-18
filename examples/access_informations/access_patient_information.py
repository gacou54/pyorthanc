from pyorthanc import Orthanc

orthanc = Orthanc('http://localhost:8042', username='orthanc', password='orthanc')

# To get patients identifier and main information
patients_identifiers = orthanc.get_patients()

for patient_identifier in patients_identifiers:
   # To get patient information
   patient_info = orthanc.get_patients_id(patient_identifier)
   patient_name = patient_info['MainDicomTags']['PatientName']
   study_identifiers = patient_info['Studies']

# To get patient's studies identifier and main information
for study_identifier in study_identifiers:
   # To get Study info
   study_info = orthanc.get_studies_id(study_identifier)
   study_date = study_info['MainDicomTags']['StudyDate']
   series_identifiers = study_info['Series']

# To get study's series identifier and main information
for series_identifier in series_identifiers:
   series_info = orthanc.get_series_id(series_identifier)
   modality = series_info['MainDicomTags']['Modality']
   instance_identifiers = series_info['Instances']

# and so on ...
for instance_identifier in instance_identifiers:
   instance_info = orthanc.get_instances_id(instance_identifier)

   # Get SOPInstanceUID
   print(instance_info['MainDicomTags']['SOPInstanceUID'])
