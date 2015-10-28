FROM python:3.4-wheezy
MAINTAINER hgi@sanger.ac.uk

COPY . /sequencescape-python-client
WORKDIR sequencescape-python-client

RUN pip install -r requirements.txt

ENTRYPOINT ["./docker/tests/run.sh"]