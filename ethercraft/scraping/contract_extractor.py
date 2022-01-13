
from os import pread
import requests
import json
import re

from ethercraft.scraping.icon_scraper import IconScraper

class Extractor():

    def __init__(self, base_url):
        self.url = base_url
        self.js_dir = base_url + 'js/'
        self.addresses = self._load_contract_addresses()
        self.contracts = {}
        for contract_name in self.addresses:
            self.contracts[contract_name] = self.load_abi_from_js(contract_name + 'ABI.js')
        self.icons = IconScraper(base_url)
        self.icons.download_all_icons()

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

    def _parse_raw_db(self, raw_text):
        raw_text = self._strip_js_from_raw(raw_text)
        last_comma_index = raw_text.rfind(',', 1)
        if last_comma_index > 0:
            # strip trailing comma
            previous_character = raw_text[last_comma_index-1]
            if previous_character == ']' or previous_character == '}':
                raw_text = raw_text[:last_comma_index] + raw_text[last_comma_index+1:]
        return json.loads(raw_text)

    def load_abi_from_js(self, abi_file_name):
        file_url = self.js_dir + abi_file_name
        req = requests.get(file_url)
        if req.status_code == 200:
            return self._parse_raw_abi(req.text)
        else:
            print(f"ABI not found for {abi_file_name}")
            return {}
    
    def load_db_from_js(self, db_file_name):
        file_url = self.js_dir + db_file_name
        req = requests.get(file_url)
        if req.status_code == 200:
            return self._parse_raw_db(req.text)
        else:
            print(f"ABI not found for {db_file_name}")
            return {}

if __name__ == '__main__':
    extractor = Extractor('https://ethercraft.io/kovan_v46/')
    res = extractor.load_db_from_js('bestiaryDB.js')
    print(res)