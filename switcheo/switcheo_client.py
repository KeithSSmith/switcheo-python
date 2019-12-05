# -*- coding:utf-8 -*-
"""
Description:
    Switcheo Client is designed to standardize interactions with the Python Client.
    It can access the Public and Authenticated Clients and is designed to be more user friendly than the
    forward facing REST API's.
    Ideally, more simplified/advanced trading functions will be built here (trailing stop, all or none, etc)
Usage:
    from switcheo.switcheo_client import SwitcheoClient
"""

from switcheo.utils import current_contract_version
from switcheo.authenticated_client import AuthenticatedClient
from switcheo.public_client import PublicClient
from switcheo.neo.utils import neo_get_scripthash_from_address

network_dict = {
    "neo": "neo",
    "NEO": "neo",
    "eth": "eth",
    "ETH": "eth",
    "ethereum": "eth",
    "Ethereum": "eth"
}

url_dict = {
    "main": 'https://api.switcheo.network/',
    "test": 'https://test-api.switcheo.network/'
}


class SwitcheoClient(AuthenticatedClient, PublicClient):

    def __init__(self,
                 switcheo_network="test",
                 blockchain_network="neo",
                 private_key=None):
        self.api_url = url_dict[switcheo_network]
        self.blockchain = network_dict[blockchain_network]
        self.contract_version = current_contract_version(
            PublicClient().get_latest_contracts()[self.blockchain.upper()], PublicClient().get_contracts())
        super().__init__(blockchain=self.blockchain,
                         contract_version=self.contract_version,
                         api_url=self.api_url)
        self.private_key = private_key

    def order_history(self, address, pair=None):
        return self.get_orders(neo_get_scripthash_from_address(address=address), pair=pair)

    def balance_current_contract(self, *addresses):
        address_list = []
        for address in addresses:
            address_list.append(neo_get_scripthash_from_address(address=address))
        return self.get_balance(addresses=address_list, contracts=self.current_contract_hash)

    def balance_by_contract(self, *addresses):
        address_list = []
        contract_dict = {}
        for address in addresses:
            address_list.append(neo_get_scripthash_from_address(address=address))
        contracts = self.get_contracts()
        for blockchain in contracts:
            contract_dict[blockchain] = {}
            for key in contracts[blockchain]:
                contract_dict[blockchain][key] =\
                    self.get_balance(addresses=address_list, contracts=contracts[blockchain][key])
        return contract_dict

    def balance_by_address_by_contract(self, *addresses):
        contract_dict = {}
        for address in addresses:
            contract_dict[address] = self.balance_by_contract(address)
        return contract_dict

    def limit_buy(self, price, quantity, pair, use_native_token=True):
        """

            limit_buy(price=0.0002, quantity=1000, pair='SWTH_NEO')
            limit_buy(price=0.0000001, quantity=1000000, pair='JRC_ETH')

        :param price:
        :param quantity:
        :param pair:
        :param use_native_token:
        :return:
        """
        if 'ETH' in pair:
            use_native_token = False
        return self.order(order_type="limit",
                          side="buy",
                          pair=pair,
                          price=price,
                          quantity=quantity,
                          private_key=self.private_key,
                          use_native_token=use_native_token)

    def limit_sell(self, price, quantity, pair, use_native_token=True):
        """

            limit_sell(price=0.0006, quantity=500, pair='SWTH_NEO')
            limit_sell(price=0.000001, quantity=100000, pair='JRC_ETH')

        :param price:
        :param quantity:
        :param pair:
        :param use_native_token:
        :return:
        """
        if 'ETH' in pair:
            use_native_token = False
        return self.order(order_type="limit",
                          side="sell",
                          pair=pair,
                          price=price,
                          quantity=quantity,
                          private_key=self.private_key,
                          use_native_token=use_native_token)

    def market_buy(self, quantity, pair, use_native_token=True):
        """

            market_buy(quantity=100, pair='SWTH_NEO')
            market_buy(quantity=100000, pair='JRC_ETH')

        :param quantity:
        :param pair:
        :param use_native_token:
        :return:
        """
        if 'ETH' in pair:
            use_native_token = False
        return self.order(order_type="market",
                          side="buy",
                          pair=pair,
                          price=0,
                          quantity=quantity,
                          private_key=self.private_key,
                          use_native_token=use_native_token)

    def market_sell(self, quantity, pair, use_native_token=True):
        """

            market_sell(quantity=100, pair='SWTH_NEO')
            market_sell(quantity=100000, pair='JRC_ETH')

        :param quantity:
        :param pair:
        :param use_native_token:
        :return:
        """
        if 'ETH' in pair:
            use_native_token = False
        return self.order(order_type="market",
                          side="sell",
                          pair=pair,
                          price=0,
                          quantity=quantity,
                          private_key=self.private_key,
                          use_native_token=use_native_token)
