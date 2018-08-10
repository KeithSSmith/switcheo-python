Public Client
^^^^^^^^^^^^^

Instantiate Class
"""""""""""""""""
::

    switcheo_pub_client = PublicClient(blockchain="neo")

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

    switcheo_pub_client.get_orders(address=neo_get_scripthash_from_private_key(prikey))

List Contract Balance for Address (ScriptHash)
""""""""""""""""""""""""""""""""""""""""""""""
::

    switcheo_pub_client.get_balance(address=neo_get_scripthash_from_private_key(prikey))

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
