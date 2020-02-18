FROM python:3.7-slim
RUN apt update && apt install -y \
    python3-dev \
    python3-pip \
    curl
COPY ./requirements.txt /usr/local/src/short_straw/
RUN pip3 install -r /usr/local/src/short_straw/requirements.txt
COPY . /usr/local/src/short_straw/
WORKDIR /usr/local/src/short_straw/
