Example of usage
----------------
Be sure that Orthanc is running. The default URL (if running locally) is `http://localhost:8042`.

Here is a list of examples to helps you getting started with pyorthanc

| Purpose                                                       | 
|---------------------------------------------------------------|
| [Access instance informations](https://github.com/ylemarechal/pyorthanc/tree/main/examples/access_informations) |
|[Transfer data from a PACS to a Orthanc server](https://github.com/ylemarechal/dicom-transfer)|

## First steps

- Applications installed
  - [x] Python3.10
  - [x] Docker

## Some useful commands

### Prepare python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pyorthanc
```


### Docker commands
Start Orthanc
```bash
docker compose up -d
```
Stop Orthanc
```bash
docker compose stop
```
Restart Orthanc
```bash
docker compose restart
```
Delete Orthanc container
```bash
docker compose down
```