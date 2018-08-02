#
# switcheo/test.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

import time
from switcheo.products import product_dict
from switcheo.authenticated_client import AuthenticatedClient
from switcheo.public_client import PublicClient
from switcheo.neo.utils import private_key_to_hex, neo_get_scripthash_from_private_key, neo_get_address_from_scripthash
from neocore.KeyPair import KeyPair
from neocore.Cryptography.Helper import scripthash_to_address
# Ideally the neo packages referencing "neo-python" could go away, these are only imported as part of
# the creation and opening of a test wallet for Switcheo.
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Wallets.utils import to_aes_key


if __name__ == "__main__":
    # wallet = UserWallet.Create(path='test_switcheo_wallet', password=to_aes_key('switcheo'))
    wallet = UserWallet.Open(path='test_switcheo_wallet', password=to_aes_key('switcheo'))
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

    switcheo_pub_client = PublicClient()
    print(switcheo_pub_client.get_candlesticks(pair="SWTH_NEO",
                                               start_time=round(time.time()) - 150000,
                                               end_time=round(time.time()),
                                               interval=1))
    print(switcheo_pub_client.get_last_24_hours())
    print(switcheo_pub_client.get_last_price())
    print(switcheo_pub_client.get_offers())
    print(switcheo_pub_client.get_trades(limit=3))
    print(switcheo_pub_client.get_pairs())
    print(switcheo_pub_client.get_pairs(base="SWTH"))

    switcheo_client = AuthenticatedClient(blockchain="neo")

    # You can only have 1 "active" deposit/withdrawal at a time, if it's still waiting
    # for the deposit confirmation you will get a 422 error until the previous deposit is complete.

    # switcheo_client.deposit(asset=product_dict["SWTH"], amount=1, kp=keypair)

    switcheo_client.withdrawal(asset="SWTH", amount=0.001, kp=keypair)

    print(switcheo_client.get_balance(neo_get_scripthash_from_private_key(prikey)))

    #### This is not working as of yet. ####
    # order = switcheo_client.create_order(kp=keypair, trade_pair="SWTH_NEO", side="buy", price=0.002,
                                         # amount=1, use_native_token=True, order_type="limit")
    # switcheo_client.execute_order(order_details=order, kp=keypair)

    #### These probably work but since the orders have yet to work these have not been tested yet. ####
    cancel = switcheo_client.create_cancellation(kp=keypair, order_id=order['id'])
    switcheo_client.execute_cancellation(kp=keypair, cancellation_details=cancel)
