FROM orthancteam/orthanc:26.11.0

RUN pip install httpx2 pydicom  --break-system-packages

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
