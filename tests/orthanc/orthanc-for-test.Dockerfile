FROM osimis/orthanc:23.9.2

RUN pip install httpx pydicom

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
