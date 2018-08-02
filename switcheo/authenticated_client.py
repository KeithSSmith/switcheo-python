#
# switcheo/authenticated_client.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

from switcheo.public_client import PublicClient
from switcheo.utils import Request, get_epoch_milliseconds
from switcheo.neo.utils import encode_message, sign_message, to_neo_asset_amount,\
    neo_get_scripthash_from_private_key, private_key_to_hex, sign_transaction


class AuthenticatedClient(PublicClient):

    def __init__(self, blockchain="neo", contract_version='V2'):
        self.request = Request(api_url='https://test-api.switcheo.network/', api_version="/v2", timeout=30)
        self.blockchain = blockchain
        self.contract_version = contract_version
        self.contract_hash = self.get_contracts()['NEO'][self.contract_version]
        self.create_signable_params = {
            'blockchain': self.blockchain,
            'asset_id': None,
            'amount': None,
            'timestamp': get_epoch_milliseconds(),
            'contract_hash': self.contract_hash
        }

    def get_balance(self, address):
        balance_params = {
            "addresses": [
                address
            ],
            "contract_hashes": [
                self.contract_hash
            ]
        }
        return self.request.get(path='/balances', params=balance_params)

    def deposit(self, asset, amount, kp):
        deposit_details = self.create_deposit(asset=asset, amount=amount, kp=kp)
        self.execute_deposit(deposit_details=deposit_details, kp=kp)

    def create_deposit(self, asset, amount, kp):
        self.create_signable_params['asset_id'] = asset
        self.create_signable_params['amount'] = str(to_neo_asset_amount(amount=amount))
        encoded_message = encode_message(self.create_signable_params)
        api_params = self.create_signable_params
        api_params['address'] = neo_get_scripthash_from_private_key(private_key=kp.PrivateKey).ToString()
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        return self.request.post(path='/deposits', json_data=api_params)

    def execute_deposit(self, deposit_details, kp):
        deposit_id = deposit_details['id']
        signature = sign_transaction(transaction=deposit_details['transaction'],
                                     private_key_hex=private_key_to_hex(key_pair=kp))
        signature = {'signature': signature}
        return self.request.post(path='/deposits/{}/broadcast'.format(deposit_id), json_data=signature)

    def withdrawal(self, asset, amount, kp):
        withdrawal_details = self.create_withdrawal(asset=asset, amount=amount, kp=kp)
        self.execute_withdrawal(withdrawal_details=withdrawal_details, kp=kp)

    def create_withdrawal(self, asset, amount, kp):
        self.create_signable_params['asset_id'] = asset
        self.create_signable_params['amount'] = str(to_neo_asset_amount(amount=amount))
        encoded_message = encode_message(self.create_signable_params)
        api_params = self.create_signable_params
        api_params['address'] = neo_get_scripthash_from_private_key(private_key=kp.PrivateKey).ToString()
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        return self.request.post(path='/withdrawals', json_data=api_params)

    def execute_withdrawal(self, withdrawal_details, kp):
        withdrawal_id = withdrawal_details['id']
        signable_params = {
            'id': withdrawal_id,
            'timestamp': get_epoch_milliseconds()
        }
        encoded_message = encode_message(signable_params)
        api_params = signable_params
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        return self.request.post(path='/withdrawals/{}/broadcast'.format(withdrawal_id), json_data=api_params)

    def create_order(self, kp, trade_pair, side, price, amount, use_native_token=True, order_type="limit"):
        signable_params = {
            "blockchain": self.blockchain,
            "pair": trade_pair,
            "side": side,
            "price": '{:.8f}'.format(price),
            "want_amount": to_neo_asset_amount(amount),
            "use_native_tokens": use_native_token,
            "order_type": order_type,
            "timestamp": get_epoch_milliseconds(),
            "contract_hash": self.contract_hash
        }
        encoded_message = encode_message(signable_params)
        api_params = signable_params
        api_params['address'] = neo_get_scripthash_from_private_key(private_key=kp.PrivateKey).ToString()
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        print(api_params)
        return self.request.post(path='/orders', json_data=api_params)

    ########  This function is not ready  ########
    def execute_order(self, order_details, kp):
        order_id = order_details['id']
        signable_params = {
            'id': withdrawal_id,
            'timestamp': get_epoch_milliseconds()
        }
        encoded_message = encode_message(signable_params)
        api_params = signable_params
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        return self.request.post(path='/orders/:id/broadcast'.format(withdrawal_id), json_data=api_params)

    def create_cancellation(self, kp, order_id):
        signable_params = {
            "order_id": order_id,
            "timestamp": get_epoch_milliseconds()
        }
        encoded_message = encode_message(signable_params)
        api_params = signable_params
        api_params['address'] = neo_get_scripthash_from_private_key(private_key=kp.PrivateKey).ToString()
        api_params['signature'] = sign_message(encoded_message=encoded_message,
                                               private_key_hex=private_key_to_hex(key_pair=kp))
        return self.request.post(path='/cancellations', json_data=api_params)

    def execute_cancellation(self, cancellation_details, kp):
        cancellation_id = cancellation_details['id']
        signature = sign_transaction(transaction=cancellation_details['transaction'],
                                     private_key_hex=private_key_to_hex(key_pair=kp))
        signature = {'signature': signature}
        return self.request.post(path='/cancellations/{}/broadcast'.format(cancellation_id), json_data=signature)
