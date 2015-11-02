# Sequencescape Python Client
[![Build Status](https://travis-ci.org/wtsi-hgi/sequencescape-python-client.svg)](https://travis-ci.org/wtsi-hgi/sequencescape-python-client)

## How To Include:
In ``/requirements.txt`` or in your ``/setup.py`` script:
```
git+https://github.com/wtsi-hgi/sequencescape-python-client.git@master
```

## How To Use:
```python
from sequencescape import connect_to_sequencescape

sequencescape = connect_to_sequencescape("mysql://user:@host:3306/database")

sequencescape.sample.get_by_name(sample_name)
sequencescape.sample.get_by_name([sample_name, other_sample_name])

sequencescape.library.get_by_id(library_internal_id)
sequencescape.library.get_by_id([library_internal_id, other_library_internal_id])

sequencescape.study.get_by_accession_number(study_accession_number)
sequencescape.study.get_by_accession_number([study_accession_number, other_study_accession_number])

sequencescape.sample.get_by_value(property, value)
sequencescape.sample.get_by_value([(property, value), (other_property, value)])
sequencescape.sample.get_by_value(property, [value, other_value])
```

## How To Develop:
### Testing
#### Locally
To run the tests, use ``./scripts/run-tests.sh`` from the project's root directory. This script will use ``pip`` to 
install all requirements for running the tests.

#### Using Docker
From the project's root directory:
```
$ docker build -t hgi/sequencescape-python-client/test -f docker/tests/Dockerfile .
$ docker run hgi/sequencescape-python-client/test
```