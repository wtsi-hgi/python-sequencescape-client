[![Build Status](https://travis-ci.org/wtsi-hgi/python-sequencescape-client.svg)](https://travis-ci.org/wtsi-hgi/python-sequencescape-client)
[![codecov.io](https://codecov.io/github/wtsi-hgi/python-sequencescape-client/coverage.svg?branch=master)](https://codecov.io/github/wtsi-hgi/python-sequencescape-client?branch=master)

# Sequencescape Python Client

## How to use in your project

### Include the `sequencescape` library
Link to use in ``/requirements.txt`` or in your ``/setup.py`` script:
```
git+https://github.com/wtsi-hgi/sequencescape-python-client.git@master#egg=sequencescape
```
*See more information about how to use packages not on PyPI in [this documentation about specifying dependencies]
(http://python-packaging.readthedocs.org/en/latest/dependencies.html#packages-not-on-pypi).*


### API
```python
from sequencescape import connect_to_sequencescape, Sample, Study, Library, \
    MultiplexedLibrary, Well, Model

# Classes of models of data in Sequencescape. Each have constructors with named parameters
available_models = [Sample, Study, Library, MultiplexedLibrary, Well]  # type: List[Model]

# Declares a connection to Sequencescape. (Actual network connections are only opened when
# required)
api = connect_to_sequencescape("mysql://user:@host:3306/database")

# Available for: study, sample, library, multiplexed_library, well
api.sample.get_by_name("sample_name")   # type: List[Sample]
api.sample.get_by_name(["sample_name", "other_sample_name"])   # type: List[Sample]

# Available for: study, sample, library, multiplexed_library, well
api.library.get_by_id(123)   # type: List[Library]
api.library.get_by_id([123, 456])   # type: List[Library]

# Available for: study, sample
api.study.get_by_accession_number("accession_number")   # type: List[Study]
api.study.get_by_accession_number(["accession_number", "other_accession_number"])   # type: List[Study]

# Available for: study, sample, library, multiplexed_library, well
api.sample.get_by_property_value("property", "value")   # type: List[Sample]
api.sample.get_by_property_value("property", ["value", "other_value"])   # type: List[Sample]
api.sample.get_by_property_value([("property", "value"), ("other_property", "other_value")])   # type: List[Sample]

# Available for: study
api.study.get_associated_with_sample(sample)  # type: List[Study]
api.study.get_associated_with_sample([sample_1, sample_2])  # type: List[Study]

# Available for: sample
api.sample.get_associated_with_study(study)  # type: List[Sample]
api.sample.get_associated_with_study([study_1, study_2])  # type: List[Sample]
```


## How to develop
### Testing
#### Locally
To run the tests, use ``./scripts/run-tests.sh`` from the project's root directory. This script will use ``pip`` to 
install all requirements for running the tests (use `virtualenv` if necessary).

#### Using Docker
From the project's root directory:
```
$ docker build -t wtsi-hgi/sequencescape-python-client/test -f docker/tests/Dockerfile .
$ docker run wtsi-hgi/sequencescape-python-client/test
```