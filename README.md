# Switcheo Python API

## Requirements
- Python 3.6 or higher with neo-python dependency (built on 3.6.5)
- Python 3.4 or higher without neo-python dependency

## Description

Alpha release of the Switcheo Python API.  This has not been tested outside of functionality and is lacking in documentation, unit testing, error handling, and standardization necessary.

The main goal of this package is to avoid using the neo-python package due to the incredibly large dependencies required to build it.  Instead we are attempting to use neo-common-python as well as extending functionality between binary and hex conversions.

Some simple examples can be found in the [test.py](test.py)

## API Examples

### Create and Open Wallet

```
wallet = UserWallet.Create(path='test_switcheo_wallet', password=to_aes_key('switcheo'))
wallet = UserWallet.Open(path='test_switcheo_wallet', password=to_aes_key('switcheo'))
```

### Extract and Transform Keys

```
wif = wallet.GetKeys()[0].Export()
prikey = KeyPair.PrivateKeyFromWIF(wif)
keypair = KeyPair(priv_key=prikey)
prikey_string = private_key_to_hex(keypair)

print(neo_get_scripthash_from_private_key(prikey))
print(type(neo_get_scripthash_from_private_key(prikey)))

print(scripthash_to_address(neo_get_scripthash_from_private_keyprikey).Data))
print(type(scripthash_to_address(neo_get_scripthash_from_privat_key(prikey).Data)))

# I don't think this is working correctly
print(neo_get_address_from_scripthash(keypair.GetAddress()))
```

### Public Client Functions

```
switcheo_pub_client = PublicClient()
print(switcheo_pub_client.get_exchange_status())
print(switcheo_pub_client.get_exchange_time())
print(switcheo_pub_client.get_orders(address=neo_get_scripthash_from_private_key(prikey)))
print(switcheo_pub_client.get_balance(neo_get_scripthash_from_private_key(prikey)))
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
```

### Authenticated Client Functions

```
switcheo_client = AuthenticatedClient(blockchain="neo")

# You can only have 1 "active" deposit/withdrawal at a time, if it's still waiting
# for the deposit confirmation you will get a 422 error until the previous deposit is complete.
print(switcheo_client.deposit(asset=product_dict["SWTH"], amount=1, kp=keypair))
# switcheo_client.withdrawal(asset=product_dict["SWTH"], amount=0.001, kp=keypair)

# Placing a limit buy order on the Switcheo/NEO trade pair
# Offering to buy 100 SWTH at the price of 0.0002 NEO for a total of 0.02 NEO
# This also uses the SWTH token to pay for any trade fees incurred on fills
order = switcheo_client.order(kp=keypair, trade_pair="SWTH_NEO", side="buy", price=0.0002,
                              amount=100, use_native_token=True, order_type="limit")

switcheo_client.cancel_order(kp=keypair, order_id=order['id'])
```

## Donation Address

NEO - ANwvg4giWPxrZeJtR3ro9TJf4dUHk5wjKe
