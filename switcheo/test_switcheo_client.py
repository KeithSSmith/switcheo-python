import unittest
from switcheo.switcheo_client import SwitcheoClient


sc = SwitcheoClient()
testnet_address1 = 'APuP9GsSCPJKrexPe49afDV8CQYubZGWd8'
testnet_address2 = 'AFqt5vxyg4KKVTcTV4sR5oYMyUGCbrMQVt'


class TestSwitcheoClient(unittest.TestCase):

    def test_order_history(self):
        orders_list = [{
            'id': 'ecb6ee9e-de8d-46d6-953b-afcc976be1ae',
            'blockchain': 'neo',
            'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
            'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
            'pair': 'SWTH_NEO',
            'side': 'buy',
            'price': '0.00001',
            'quantity': '1000000000000',
            'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
            'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
            'offer_amount': '6000000',
            'want_amount': '30000000000',
            'transfer_amount': '0',
            'priority_gas_amount': '0',
            'use_native_token': True,
            'native_fee_transfer_amount': 0,
            'deposit_txn': None,
            'created_at': '2018-08-08T18:39:13.864Z',
            'status': 'processed',
            'order_status': 'cancelled',
            'txn': None,
            'offer_asset_blockchain': 'neo',
            'want_asset_blockchain': 'neo',
            'broadcast_cutoff_at': '2019-05-04T15:53:04.809Z',
            'scheduled_cancellation_at': None,
            'counterpart_swap': None,
            "unlock_swap_txn": None,
            'fills': [],
            'fill_groups': [],
            'makes': []
            }]
        orders_list = orders_list[0].keys()
        all_orders = sc.order_history(address=testnet_address1)
        self.assertTrue(set(all_orders[0].keys()).issubset(set(orders_list)))

    def test_balance_current_contract(self):
        expected_balance_current_contract_child_key_set = set(['confirming', 'confirmed', 'locked'])
        balance_current_contract = sc.balance_current_contract(testnet_address1)
        balance_current_contract_child_key_set = set(balance_current_contract.keys())
        self.assertTrue(
            balance_current_contract_child_key_set.issubset(expected_balance_current_contract_child_key_set))

    def test_balance_by_contract(self):
        expected_balance_by_contract_key_set = set(['NEO', 'ETH', 'QTUM', 'EOS'])
        expected_balance_by_contract_child_key_set = set(['V1', 'V1_5', 'V2', 'V3'])
        expected_balance_by_contract_sub_key_set = set(['confirming', 'confirmed', 'locked'])
        balance_by_contract = sc.balance_by_contract(testnet_address1)
        balance_by_contract_key_set = set(balance_by_contract.keys())
        self.assertTrue(balance_by_contract_key_set.issubset(expected_balance_by_contract_key_set))
        balance_by_contract_neo = balance_by_contract['NEO']
        balance_by_contract_eth = balance_by_contract['ETH']
        balance_by_contract_child_key_set = set(balance_by_contract_neo.keys())
        self.assertTrue(balance_by_contract_child_key_set.issubset(expected_balance_by_contract_child_key_set))
        balance_by_contract_sub_key_set = set(balance_by_contract_neo['V1'])
        self.assertTrue(balance_by_contract_sub_key_set.issubset(expected_balance_by_contract_sub_key_set))
        balance_by_contract_child_key_set = set(balance_by_contract_eth.keys())
        self.assertTrue(balance_by_contract_child_key_set.issubset(expected_balance_by_contract_child_key_set))
        balance_by_contract_sub_key_set = set(balance_by_contract_eth['V1'])
        self.assertTrue(balance_by_contract_sub_key_set.issubset(expected_balance_by_contract_sub_key_set))

    def test_balance_by_address_by_contract(self):
        expected_balance_by_address_key_set = set([testnet_address1, testnet_address2])
        balance_by_address_key_set = set(sc.balance_by_address_by_contract(testnet_address1, testnet_address2).keys())
        self.assertTrue(balance_by_address_key_set.issubset(expected_balance_by_address_key_set))
