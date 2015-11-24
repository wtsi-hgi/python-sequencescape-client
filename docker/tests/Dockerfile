FROM python:3.5
MAINTAINER Colin Nolan <hgi@sanger.ac.uk>

COPY . /sequencescape-python-client
WORKDIR sequencescape-python-client

RUN pip install -r requirements.txt
RUN pip install -r test_requirements.txt

CMD ["./scripts/run-tests.sh"]