ARG ORTHANC_VERSION

FROM orthancteam/orthanc:${ORTHANC_VERSION}

MAINTAINER Yannick Lemaréchal <yannick.lemarechal.1@ulaval.ca>
LABEL Description="Orthanc with pyorthanc"
LABEL org.opencontainers.image.authors="Gabriel Couture, Yannick Lemaréchal"
LABEL org.label-schema.url="https://github.com/gacou54/pyorthanc"

RUN apt-get -y clean && \
    apt-get -y update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    python3.11 python3.11-full

ARG PYORTHANC_VERSION

RUN pip install --break-system-packages pyorthanc==${PYORTHANC_VERSION}