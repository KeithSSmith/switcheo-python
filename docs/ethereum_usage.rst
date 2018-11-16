Ethereum Signatures
^^^^^^^^^^^^^^^^^^^

The Switcheo docs go into extensive detail about how to authenticate messages (https://docs.switcheo.network/#authentication) on the NEO blockchain.  These complications have been abstracted to make it easier for the developer to use to allow for quicker development of their project.

This also means it is no longer necessary to run both ``create`` and ``execute`` portions of the authenticated client tasks since both are handled with the higher level functions listed below.

Sign Create Cancellation
""""""""""""""""""""""""
::

    sign_create_cancellation(cancellation_params, private_key)

Sign Execute Cancellation
"""""""""""""""""""""""""
::

    sign_execute_cancellation(cancellation_params, private_key)

Sign Create Deposit
"""""""""""""""""""
::

    sign_create_deposit(deposit_params, private_key)

Sign Execute Deposit
""""""""""""""""""""
::

    sign_execute_deposit(deposit_params, private_key, infura_url)

Sign Create Order
"""""""""""""""""
::

    sign_create_order(order_params, private_key)

Sign Execute Order
""""""""""""""""""
::

    sign_execute_order(order_params, private_key)

Sign Create Withdrawal
""""""""""""""""""""""
::

    sign_create_withdrawal(withdrawal_params, private_key)

Sign Execute Withdrawal
"""""""""""""""""""""""""
::

    sign_execute_withdrawal(withdrawal_params, private_key)
