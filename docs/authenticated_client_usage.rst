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
