#
# Musixmatch Model Hub
# @author Loreto Parisi (loreto at musixmatch dot com)
# Copyright (c) 2020 Loreto Parisi
#

FROM python:3.7.4-slim-buster

LABEL maintainer Loreto Parisi loreto@musixmatch.com

WORKDIR app

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential

# app requirements
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# app
COPY src/* ./

CMD ["bash"]