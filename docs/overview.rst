========
Overview
========

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


Rate Limits
^^^^^^^^^^^

All endpoints are rate-limited by the Switcheo team.  Hard and fast rules are not given but it has been stated that open transactions (unsigned) and transactions that have not hit the blockchain will attribute to this limit.

The error code ``429`` will indicate when a rate limit has been met.  It is important for the developer to implement an exponential back off strategy when encountering this error code.

Further error codes can be found at https://docs.switcheo.network/#error
