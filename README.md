# Sequencescape Python Client
[![Build Status](https://travis-ci.org/wtsi-hgi/sequencescape-python-client.svg)](https://travis-ci.org/wtsi-hgi/sequencescape-python-client)

## How to use in your project
### Including the `sequencescape` library
In ``/requirements.txt`` or in your ``/setup.py`` script:
```
git+https://github.com/wtsi-hgi/sequencescape-python-client.git@master#egg=sequencescape
```
*See more about using libraries for git repositories in the 
[pip documentation](https://pip.readthedocs.org/en/1.1/requirements.html#git).*

## API
```python
from sequencescape import connect_to_sequencescape, Sample, Study, Library, \
    MultiplexedLibrary, Well, Model

# Classes of models of data in Sequencescape. Each have constructors with named parameters
available_models = [Sample, Study, Library, MultiplexedLibrary, Well]   # type: List[Model]

# Declares a connection to Sequencescape. (Actual network connections are only opened when
# required)
sequencescape = connect_to_sequencescape("mysql://user:@host:3306/database")

# Available for: study, sample, library, multiplexed_library, well
sequencescape.sample.get_by_name(sample_name)   # type: List[Sample]
sequencescape.sample.get_by_name([sample_name, other_sample_name])   # type: List[Sample]

# Available for: study, sample, library, multiplexed_library, well
sequencescape.library.get_by_id(library_id)   # type: List[Library]
sequencescape.library.get_by_id([library_id, other_library_id])   # type: List[Library]

# Available for: study, sample
sequencescape.study.get_by_accession_number(study_accession_number)   # type: List[Study]
sequencescape.study.get_by_accession_number(
    [study_accession_number, other_study_accession_number])   # type: List[Study]

# Available for: study
sequencescape.study.get_associated_with_sample(sample)  # type: List[Study]
sequencescape.study.get_associated_with_sample([sample_1, sample_2])  # type: List[Study]

# Available for: sample
sequencescape.sample.get_associated_with_study(study)  # type: List[Sample]
sequencescape.sample.get_associated_with_study([study_1, study_2])  # type: List[Sample]
```


## How to develop
### Testing
#### Locally
To run the tests, use ``./scripts/run-tests.sh`` from the project's root directory. This script will use ``pip`` to 
install all requirements for running the tests (use `virtualenv` if necessary).

#### Using Docker
From the project's root directory:
```
$ docker build -t hgi/sequencescape-python-client/test -f docker/tests/Dockerfile .
$ docker run hgi/sequencescape-python-client/test
```