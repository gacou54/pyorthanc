# Acces to patient-study-series-instance informations

In this tutorial, you can access to all patients, study, series and instances information. Use it with a small batch of 
data in the Orthanc server

## Get the python file
[access_patient_information.py](./access_patient_information.py)
[docker-compose.yaml](./docker-compose.yaml)

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

## Run PyOrthanc script
```bash
python access_patient_information.py
```