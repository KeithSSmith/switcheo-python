#
# switcheo/public_client.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

from switcheo.utils import Request


class PublicClient(object):

    def __init__(self, blockchain="neo"):
        self.request = Request(api_url='https://test-api.switcheo.network/', api_version="/v2", timeout=30)
        self.blockchain = blockchain

    def get_exchange_status(self):
        return self.request.status()

    def get_exchange_time(self):
        return self.request.get(path='/exchange/timestamp')

    def get_candlesticks(self, pair, start_time, end_time, interval):
        candle_params = {
            "pair": pair,
            "interval": interval,
            "start_time": start_time,
            "end_time": end_time
        }
        return self.request.get(path='/tickers/candlesticks', params=candle_params)

    def get_last_24_hours(self):
        return self.request.get(path='/tickers/last_24_hours')

    def get_last_price(self):
        return self.request.get(path='/tickers/last_price')

    def get_offers(self, trade_pair="SWTH_NEO"):
        offer_params = {
            "blockchain": self.blockchain,
            "pair": trade_pair,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        return self.request.get(path='/offers', params=offer_params)

    def get_trades(self, trade_pair="SWTH_NEO", start_time='', end_time='', limit=5000):
        if limit > 10000 or limit < 1:
            exit()
        trades_params = {
            "blockchain": self.blockchain,
            "pair": trade_pair,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        if start_time != '':
            trades_params['from'] = start_time
        if end_time != '':
            trades_params['to'] = end_time
        if limit != 5000:
            trades_params['limit'] = limit
        return self.request.get(path='/trades', params=trades_params)

    def get_pairs(self, base=''):
        if base in ["NEO", "GAS", "SWTH", "USD"]:
            base_params = {
                "bases": [
                    base
                ]
            }
            return self.request.get(path='/pairs', params=base_params)
        else:
            return self.request.get(path='/pairs')

    def get_contracts(self):
        return self.request.get(path='/contracts')

    def get_orders(self, address):
        order_params = {
            "address": address,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        return self.request.get(path='/orders', params=order_params)

    def get_balance(self, address):
        balance_params = {
            "addresses": [
                address
            ],
            "contract_hashes": [
                self.get_contracts()["NEO"]["V2"]
            ]
        }
        return self.request.get(path='/balances', params=balance_params)
