FROM python:3.4-wheezy
MAINTAINER hgi@sanger.ac.uk

COPY . /sequencescape-python-client
WORKDIR sequencescape-python-client

RUN ./scripts/pip-install-requirements.sh

CMD ["./scripts/run-tests.sh"]