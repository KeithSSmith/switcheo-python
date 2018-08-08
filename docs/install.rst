Installation
------------

This package is designed to be light weight and is not designed to create or store NEO wallets.  If this is required for your application please refer to the `neo-python` (https://github.com/CityOfZion/neo-python) project for your needs.

Requirements
^^^^^^^^^^^^

- Python 3.5 or greater

Environment Setup
^^^^^^^^^^^^^^^^^

Python Installation
"""""""""""""""""""
Since this project requires Python 3.5 or greater this can be installed via the recommended methods found at https://www.python.org/downloads/


``virtualenv`` Dependency Management
""""""""""""""""""""""""""""""""""""

It is also highly recommended to use the ``virtualenv`` functionality allowing the developer to isolate dependencies between projects.  For more information the following link is worth reading: https://docs.python-guide.org/dev/virtualenvs/

Docker Image
""""""""""""

This project also comes with a simple Docker file that can be used to execute the contents of this package inside of.  This package was developed inside of the Docker container so if there are any issues during use please report them.

Install with ``pip``
^^^^^^^^^^^^^^^^^^^^
::

    python -m pip install switcheo

Install from PyPi
^^^^^^^^^^^^^^^^^

The easiest way to install ``switcheo`` on your machine is to download it and install from PyPi using ``pip``. First, we recommend you to create a virtual environment in order to isolate this installation from your system directories and then install it as you normally would do:

  ::

    # create project dir
    mkdir myproject
    cd myproject

    # create virtual environment and activate

    python3.6 -m venv venv # this can also be python3 -m venv venv depending on your environment
    source venv/bin/activate

    (venv) pip install switcheo


Install from Git
^^^^^^^^^^^^^^^^

Clone the repository at `https://github.com/KeithSSmith/switcheo-python <https://github.com/KeithSSmith/switcheo-python>`_ and navigate into the project directory.
Make a Python 3 virtual environment and activate it via

::

    python3.6 -m venv venv
    source venv/bin/activate

Then install the requirements via

::

    pip install -U setuptools pip wheel
    pip install -e .


Updating switcheo-python from Git
"""""""""""""""""""""""""""""""""

If you are updating switcheo-python with ``git pull``, make sure you also update the dependencies with ``pip install -r requirements.txt``.
