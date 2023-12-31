=============
DemoProject
=============


.. image:: https://img.shields.io/pypi/v/exceptiontest.svg
        :target: https://pypi.python.org/pypi/exceptiontest

.. image:: https://img.shields.io/travis/rp926463-arch/exceptiontest.svg
        :target: https://travis-ci.com/rp926463-arch/exceptiontest

.. image:: https://readthedocs.org/projects/exceptiontest/badge/?version=latest
        :target: https://exceptiontest.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




This script is to demonstrate best practices to implement exception handing, logging, command line argument parsers & test cases using unittest python.


* Free software: license
* Documentation: https://demoproject.readthedocs.io.


Features
--------

* Best practices to do `exception handling <https://docs.python.org/3/tutorial/errors.html#exceptions>`_ (python).
* Best practices for `logging <https://docs.python.org/3/howto/logging.html>`_ (python).
* Best practices to handle command line arguments using `argparser <https://docs.python.org/3/library/argparse.html>`_ (python).
* Best practices to write test cases using `unittest <https://docs.python.org/3/library/unittest.html>`_ - build in testing library (python).

1. Unittest
    pip install coverage

    commands :
        - python -m unittest tests.unit.test_fileprocessor
        - python -m unittest discover -->  command is used to discover and run all tests in a project.
        - coverage run -m unittest discover
        - coverage report -m --> generate .coverage file & show report in sys.out
        - coverage html --> generate html report of coverage

    Note : `Exclusion and Inclusion <https://coverage.readthedocs.io/en/7.4.0/source.html#source>`_ criteria can be added in .coveragerc file (it has to be placed in the basepath)

Contributors
------------

None yet. Why not be the first?


History
------------

0.1.0 (2023-12-28)

* First release on PyPI.
