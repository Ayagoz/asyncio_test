FROM ubuntu:22.04 as base
WORKDIR /workdir
COPY . /workdir

RUN apt update
RUN apt install python3 python3-pip -y

RUN cd /workdir && \
    echo "$(python3 --version)" && \
    pip3 install -r requirements.txt
