FROM orthancteam/orthanc:24.12.0

RUN pip install httpx pydicom  --break-system-packages

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
