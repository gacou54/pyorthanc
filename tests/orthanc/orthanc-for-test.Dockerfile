FROM orthancteam/orthanc:24.5.1

RUN pip install httpx pydicom  --break-system-packages

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
