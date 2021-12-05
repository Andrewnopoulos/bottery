
import requests
import json
import re

class Extractor():

    def __init__(self, base_url):
        self.url = base_url
        self.js_dir = base_url + 'js/'
        self.addresses = self._load_contract_addresses()
        self.contracts = {}
        for contract_name in self.addresses:
            self.contracts[contract_name] = self.load_abi_from_js(contract_name + 'ABI.js')

    def _load_contract_addresses(self):
        file_url = self.js_dir + 'contracts.js'
        req = requests.get(file_url)
        if req.status_code == 200:
            raw_address_list = req.text
            stripped = self._strip_js_from_raw(raw_address_list)
            addresses = dict(re.findall(r'([a-z]+):"(0x[a-zA-Z0-9]+)"', stripped))
            return addresses

    def _strip_js_from_raw(self, raw_text):
        raw_text = raw_text.split('=')[1]
        raw_text = raw_text.rsplit(';', 1)[0]
        return raw_text

    def _parse_raw_abi(self, raw_text):
        as_json = json.loads(self._strip_js_from_raw(raw_text))
        return as_json

    def load_abi_from_js(self, abi_file_name):
        file_url = self.js_dir + abi_file_name
        req = requests.get(file_url)
        if req.status_code == 200:
            return self._parse_raw_abi(req.text)
        else:
            print(f"ABI not found for {abi_file_name}")
            return {}

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    from web3 import Web3
    load_dotenv()
    ETHERCRAFT_KOVAN_URL = os.getenv('ETHERCRAFT_KOVAN_URL')
    KOVAN_ENDPOINT = os.getenv('KOVAN_ENDPOINT')
    CHARACTER_ADDRESS = os.getenv('CHARACTER_ADDRESS')

    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    extractor = Extractor(ETHERCRAFT_KOVAN_URL)
    res = extractor.load_abi_from_js('characterABI.js')
    contr = w3.eth.contract(address=CHARACTER_ADDRESS, abi=res)
    print(res)