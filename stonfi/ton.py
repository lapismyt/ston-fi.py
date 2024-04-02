import requests
import json
import codecs

class ToncenterClient:
    def __init__(self, api_key, testnet=False):
        self.api_key = api_key
        if testnet:
            self.base_url = 'https://testnet.toncenter.com/api/v3/'
        else:
            self.base_url = 'https://toncenter.com/api/v3/'

    def _run(self, endpoint, method, data={}):
        url = self.base_url + endpoint
        headers = {'X-API-Key': self.api_key}
        if method.upper() == 'GET':
            response = requests.get(url, params=data, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            raise Exception('Not supported HTTP method.')
        return response.json()

    def send_message(self, boc):
        boc = codecs.decode(codecs.encode(boc, 'base64'), 'utf-8')
        response = self._run('message', 'POST', {'boc': boc})
        return response

    def run_get_method(self, address, method, stack=[]):
        data = {
            'address': address,
            'method': method,
            'stack': stack
        }
        response = self._run('runGetMethod', 'POST', data)
        return response

    def get_account_info(self, address):
        response = self._run('account', 'GET', {'address': address})
        return response

    def get_wallet_info(self, address):
        response = self._run('wallet', 'GET', {'address': address})
        return response

    def get_transactions(self,
                         account=None,
                         limit=128,
                         offset=0,
                         exclude_account=None,
                         start_utime=None,
                         end_utime=None,
                         workchain=None,
                         shard=None,
                         seqno=None,
                         hash=None,
                         lt=None,
                         sort='desc',
                         start_lt=None,
                         end_lt=None):
        data_raw = {
            'account': account,
            'limit': limit,
            'offset': offset,
            'exclude_account': exclude_account,
            'start_utime': start_utime,
            'end_utime': end_utime,
            'workchain': workchain,
            'shard': shard,
            'seqno': seqno,
            'hash': hash,
            'lt': lt,
            'sort': sort,
            'start_lt': start_lt,
            'end_lt': end_lt
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('transactions', 'GET', data)
        return response

    def get_messages(self,
                     hash=None,
                     source=None,
                     destination=None,
                     body_hash=None,
                     limit=128,
                     offset=0):
        data_raw = {
            'hash': hash,
            'source': source,
            'destination': destination,
            'body_hash': body_hash,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('messages', 'GET', data)
        return response

    def get_nft_collections(self,
                            collection_address=None,
                            owner_address=None,
                            limit=128,
                            offset=0):
        data_raw = {
            'collection_address': collection_address,
            'owner_address': owner_address,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('nft/collections', 'GET', data)
        return response
    
    def get_nft_items(self,
                      address=None,
                      owner_address=None,
                      collection_address=None,
                      limit=128,
                      offset=0):
        data_raw = {
            'address': address,
            'owner_address': owner_address,
            'collection_address': collection_address,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('nft/items', 'GET', data)
        return response

    def get_nft_transfers(self,
                          address=None,
                          item_address=None,
                          collection_address=None,
                          direction='both', # in, out, both
                          start_utime=None,
                          end_utime=None,
                          start_lt=None,
                          end_lt=None,
                          limit=128,
                          offset=0):
        data_raw = {
            'address': address,
            'item_address': item_address,
            'collection_address': collection_address,
            'direction': direction,
            'start_utime': start_utime,
            'end_utime': end_utime,
            'start_lt': start_lt,
            'end_lt': end_lt,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('nft/transfers', 'GET', data)
        return response

    def get_jetton_masters(self,
                           address=None,
                           admin_address=None,
                           limit=128,
                           offset=0):
        data_raw = {
            'address': address,
            'admin_address': admin_address,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('jetton/masters', 'GET', data)
        return response

    def get_jetton_wallets(self,
                           address=None,
                           owner_address=None,
                           jetton_address=None,
                           limit=128,
                           offset=0):
        data_raw = {
            'address': address,
            'owner_address': owner_address,
            'jetton_address': jetton_address,
            'limit': limit,
            'offset': offset
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('jetton/wallets', 'GET', data)
        return response

    def get_jetton_transfers(self,
                             address=None,
                             jetton_wallet=None,
                             jetton_master=None,
                             direction='both', # in, out, both
                             start_utime=None,
                             end_utime=None,
                             start_lt=None,
                             end_lt=None,
                             limit=128,
                             offset=0,
                             sort='desc'):
        data_raw = {
            'address': address,
            'jetton_wallet': jetton_wallet,
            'jetton_master': jetton_master,
            'direction': direction,
            'start_utime': start_utime,
            'end_utime': end_utime,
            'start_lt': start_lt,
            'end_lt': end_lt,
            'limit': limit,
            'offset': offset,
            'sort': sort
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('jetton/transfers', 'GET', data)
        return response

    def get_jetton_burns(self,
                         address=None,
                         jetton_wallet=None,
                         jetton_master=None,
                         start_utime=None,
                         end_utime=None,
                         start_lt=None,
                         end_lt=None,
                         limit=128,
                         offset=0,
                         sort='desc'):
        data_raw = {
            'address': address,
            'jetton_wallet': jetton_wallet,
            'jetton_master': jetton_master,
            'start_utime': start_utime,
            'end_utime': end_utime,
            'start_lt': start_lt,
            'end_lt': end_lt,
            'limit': limit,
            'offset': offset,
            'sort': sort
        }
        data = {}
        for item in data_raw.keys():
            if data_raw[item] is not None:
                data[item] = data_raw[item]
        response = self._run('jetton/burns', 'GET', data)
        return response

