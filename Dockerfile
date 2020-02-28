FROM fnndsc/ubuntu-python3
RUN apt-get update
RUN apt-get update && apt-get install -y libxft-dev libfreetype6 libfreetype6-dev
COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY cassowary/ /cassowary

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8