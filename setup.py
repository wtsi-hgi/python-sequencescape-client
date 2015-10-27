from distutils.core import setup

setup(
    name="sequencescape-python-client",

    version="0.1.0",

    author="Colin Nolan",
    author_email="hgi@sanger.ac.uk",

    packages=["sequencescape", "sequencescape.sqlalchemy"],

    include_package_data=False,

    url="https://github.com/wtsi-hgi/sequencescape-python-client",

    license="LICENSE",

    description="Python client for interfacing with a Sequencescape database.",
    long_description=open("README").read(),

    install_requires=[
        "SQLAlchemy==1.0.9",
        "mysqlclient==1.3.6"
    ],

    test_suite="sequencescape/tests"
)