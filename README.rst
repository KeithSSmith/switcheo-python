===================
Switcheo Python API
===================

Python Client for interacting with the Switcheo API.

.. image:: https://readthedocs.org/projects/switcheo-python/badge/?version=latest
    :target: https://switcheo-python.readthedocs.io/en/latest
    :alt: ReadTheDocs
.. image:: https://travis-ci.org/KeithSSmith/switcheo-python.svg?branch=master
    :target: https://travis-ci.org/KeithSSmith/switcheo-python
    :alt: Travis CI
.. image:: https://coveralls.io/repos/github/KeithSSmith/switcheo-python/badge.svg?branch=master
    :target: https://coveralls.io/github/KeithSSmith/switcheo-python?branch=master
    :alt: Coveralls
.. image:: https://img.shields.io/pypi/v/switcheo.svg
    :target: https://pypi.org/project/switcheo
    :alt: PyPi
.. image:: https://img.shields.io/pypi/pyversions/switcheo.svg
    :target: https://pypi.org/project/switcheo
    :alt: PyPi
.. image:: https://img.shields.io/pypi/l/switcheo.svg
    :target: https://img.shields.io/pypi/l/switcheo.svg
    :alt: PyPi

Table of Contents
-----------------

- `Overview`_
- `Installation`_
- `Public Client`_
- `Authenticated  Client`_
- `Donations`_

Overview
--------

Introduction
^^^^^^^^^^^^

This library is intended to empower developers to more easily interact with the Switcheo Decentralized Exchange through simple Python interfaces.

Switcheo is the first functional DEX in the NEO Smart Economy and with the version 2 release of its platform made an API endpoint widely available for developers to build on top of it.  This package is a wrapper around the API endpoints and is attempting to replicate and expand on the original functions available.

The official Switcheo documentation can be found at https://docs.switcheo.network/

API Requests
^^^^^^^^^^^^

The Switcheo API uses REST architecture to server data through its endpoints.  The requests and responses of the endpoint use JSON format.

While the endpoint returns JSON this package turns the request into a Python dictionary for easier interoperability and function lookup.

There are two type of API endpoints presented in this package:

- Public APIs (Switcheo docs refers to Exchange APIs) - do not require authentication (message signing) that provide access to exchange history, statistics, state, and various other information about the exchange.
- Authenticated APIs (Switcheo docs refers to Trading APIs) - do require authentication and these endpoints include deposits, withdrawals, trading, and cancellation.

Mainnet and Testnet Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When developing an application it is best to do testing against the Testnet endpoints, these can be found at:

+-----+----------------------------------+
|     | URL                              |
+=====+==================================+
|UI   | https://beta.switcheo.exchange   |
+-----+----------------------------------+
|API  | https://test-api.switcheo.network|
+-----+----------------------------------+

For live market data and trading on the mainnet the following enpoints should be used:

+-----+----------------------------------+
|     | URL                              |
+=====+==================================+
|UI   | https://switcheo.exchange        |
+-----+----------------------------------+
|API  | https://api.switcheo.network     |
+-----+----------------------------------+

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

Public Client
^^^^^^^^^^^^^

Instantiate Class
"""""""""""""""""
::

    switcheo_pub_client = PublicClient(blockchain=neo)

Exchange API Status
"""""""""""""""""""
::

    switcheo_pub_client.get_exchange_status()

Exchange Time in Epoch Milliseconds
"""""""""""""""""""""""""""""""""""
::

    switcheo_pub_client.get_exchange_time()

List Smart Contract Hashes
""""""""""""""""""""""""""
::

    switcheo_pub_client.get_contracts()


List Trade Pairs
""""""""""""""""
::

    switcheo_pub_client.get_pairs()
    switcheo_pub_client.get_pairs(base="SWTH")

List Orders for Address (ScriptHash)
""""""""""""""""""""""""""""""""""""
::

    switcheo_pub_client.get_orders(address=neo_get_scripthash_from_address(address))

List Contract Balance for Address (ScriptHash)
""""""""""""""""""""""""""""""""""""""""""""""
::

    switcheo_pub_client.get_balance(address=neo_get_scripthash_from_address(address))

Tickers
"""""""
::

    switcheo_pub_client.get_candlesticks(pair="SWTH_NEO", start_time=round(time.time()) - 350000, end_time=round(time.time()), interval=360))
    switcheo_pub_client.get_last_24_hours()
    switcheo_pub_client.get_last_price()

Offers on Order Book
""""""""""""""""""""
::

    switcheo_pub_client.get_offers(pair="GAS_NEO")

Executed Trades for a Given Pair
""""""""""""""""""""""""""""""""
::

    switcheo_pub_client.get_trades(pair="SWTH_NEO", limit=3)

Authenticated Client
^^^^^^^^^^^^^^^^^^^^

The Switcheo docs go into extensive detail about how to authenticate messages (https://docs.switcheo.network/#authentication) on the NEO blockchain.  These complications have been abstracted to make it easier for the developer to use to allow for quicker development of their project.

This also means it is no longer necessary to run both ``create`` and ``execute`` portions of the authenticated client tasks since both are handled with the higher level functions listed below.

Instantiate Class
"""""""""""""""""
::

    switcheo_client = AuthenticatedClient(blockchain="neo")

Deposit to Smart Contract
"""""""""""""""""""""""""
::

    switcheo_client.deposit(asset=product_dict["SWTH"], amount=1, kp=kp)

Withdrawal from Smart Contract
""""""""""""""""""""""""""""""
::

    switcheo_client.withdrawal(asset=product_dict["SWTH"], amount=0.001, kp=kp)

Place a Limit Order
"""""""""""""""""""
::

    switcheo_client.order(kp=kp, pair="SWTH_NEO", side="buy", price=0.0002, amount=100, use_native_token=True, order_type="limit")

Cancel an Open Order
""""""""""""""""""""
::

    switcheo_client.cancel_order(order_id=order['id'], kp=kp)

Donations
---------

Accepted at Neo address **ANwvg4giWPxrZeJtR3ro9TJf4dUHk5wjKe**.

.. _MIT: https://github.com/KeithSSmith/switcheo-python/blob/master/LICENSE.md
