FROM osimis/orthanc:22.6.1

RUN pip install httpx pydicom

COPY pyorthanc /python/pyorthanc
COPY tests/orthanc/script.py /python/script.py
