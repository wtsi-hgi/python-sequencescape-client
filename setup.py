from setuptools import setup, find_packages

setup(
    name="sequencescape",

    version="0.1.6",

    author="Colin Nolan",
    author_email="hgi@sanger.ac.uk",

    packages=find_packages(exclude=["tests"]),

    url="https://github.com/wtsi-hgi/python-sequencescape-client",

    license="LICENSE.txt",

    description="Python client for interfacing with a Sequencescape database.",
    long_description=open("README.md").read(),

    install_requires=[x for x in open("requirements.txt").read().splitlines() if "://" not in x],
    dependency_links=[x for x in open("requirements.txt").read().splitlines() if "://" in x],

    test_suite="sequencescape.tests"
)
