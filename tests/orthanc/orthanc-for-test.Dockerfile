FROM orthancteam/orthanc:24.2.0

RUN pip install httpx pydicom

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
