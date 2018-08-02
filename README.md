# Switcheo Python API

## Requirements
- Python 3.6 or higher with neo-python dependency (built on 3.6.5)
- Python 3.4 or higher without neo-python dependency

## Description

An initial release of the Switcheo Python API.  This has not been tested and is lacking in documentation, unit testing, error handling, and standardization.

The main goal of this package is to avoid using the neo-python package due to the incredibly large dependencies required to build it.  Instead we are attempting to use neo-common-python as well as extending functionality between binary and hex conversions.

Some simple examples can be found in the [test.py](test.py)

**Create and Open Wallet**

    wallet = UserWallet.Create(path='test_switcheo_wallet', password=to_aes_key('switcheo'))
    wallet = UserWallet.Open(path='test_switcheo_wallet', password=to_aes_key('switcheo'))

**Extract and Transform Keys**

    wif = wallet.GetKeys()[0].Export()
    prikey = KeyPair.PrivateKeyFromWIF(wif)
    keypair = KeyPair(priv_key=prikey)
    prikey_string = private_key_to_hex(keypair)

    print(neo_get_scripthash_from_private_key(prikey))
    print(type(neo_get_scripthash_from_private_key(prikey)))

    print(scripthash_to_address(neo_get_scripthash_from_private_key(prikey).Data))
    print(type(scripthash_to_address(neo_get_scripthash_from_private_key(prikey).Data)))

    # I don't think this is working correctly
    print(neo_get_address_from_scripthash(keypair.GetAddress()))

**Public Client Functions**

    switcheo_pub_client = PublicClient()
    switcheo_pub_client.get_candlesticks(pair="SWTH_NEO",
                                         start_time=round(time.time()) - 150000,
                                         end_time=round(time.time()),
                                         interval=1)
    switcheo_pub_client.get_last_24_hours()
    switcheo_pub_client.get_last_price()
    switcheo_pub_client.get_offers()
    switcheo_pub_client.get_trades(limit=3)
    switcheo_pub_client.get_pairs()
    switcheo_pub_client.get_pairs(base="SWTH")

**Authenticated Client Functions**

    switcheo_client = AuthenticatedClient(blockchain="neo")

    # You can only have 1 "active" deposit/withdrawal at a time, if it's still waiting
    # for the deposit confirmation you will get a 422 error until the previous deposit is complete.

    switcheo_client.deposit(asset=product_dict["SWTH"], amount=1, kp=keypair)

    switcheo_client.withdrawal(asset="SWTH", amount=0.001, kp=keypair)

    switcheo_client.get_balance(neo_get_scripthash_from_private_key(prikey))

    #### This is not working as of yet. ####
    # order = switcheo_client.create_order(kp=keypair, trade_pair="SWTH_NEO", side="buy", price=0.002,
    #                                      amount=1, use_native_token=True, order_type="limit")
    # switcheo_client.execute_order(order_details=order, kp=keypair)

    #### These probably work but since the orders have yet to work these have not been tested yet. ####
    cancel = switcheo_client.create_cancellation(kp=keypair, order_id=order['id'])
    switcheo_client.execute_cancellation(kp=keypair, cancellation_details=cancel)
