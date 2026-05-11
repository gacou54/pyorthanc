FROM orthancteam/orthanc:26.4.2

RUN pip install httpx pydicom  --break-system-packages

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
