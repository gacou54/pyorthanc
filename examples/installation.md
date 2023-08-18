## First steps

- Applications installed
  - [x] Python3.10
  - [x] Docker


## Prepare Orthanc
For the examples, we use a vanilla Orthanc inside a docker. The first step is to prepare a dedicated directory,
and copy/past the below code in a file called ```docker-compose.yaml```
```yaml
version: '3.3'
services:
  orthanc:
    image: jodogne/orthanc-plugins:1.12.1
    ports:
      - 4242:4242
      - 8042:8042
```
You can also dowload it directly from this [link](./docker-compose.yaml)

## Run Orthanc

To run a local Orthanc with Docker, just run this command in the same directory of your ```docker-compose.yaml``` file

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

