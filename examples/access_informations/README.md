# Acces to patient-study-series-instance informations


## Run Orthanc

To run a local Orthanc with Docker, just run 
```bash
docker compose up -d
```

The default URL (if running locally) is `http://localhost:8042`.

## Prepare environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pyorthanc
```

## Get the python file
[access_patient_information.py](./access_patient_information.py)

## Acces to patient-study-series-instance informatios
```bash
python access_patient_information.py
```
