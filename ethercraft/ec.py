from logging import addLevelName
import os, json
from web3 import Web3
from ethercraft.scraping import Extractor

from dotenv import load_dotenv
load_dotenv()
KOVAN_ENDPOINT = os.getenv('KOVAN_ENDPOINT')
MAINNET_ENDPOINT = os.getenv('MAINNET_ENDPOINT')

class Ethercraft():

    def load_settings(self):
        settings_path = "ethercraft/static/settings.json"
        with open(settings_path, 'r') as settings_file:
            self.settings = json.load(settings_file)

    def __init__(self, version="kovan"):
        self.load_settings()
        self.base_url = self.settings['main'] + self.settings['versions'].get(version, 'kovan_v46') + "/"
        endpoint = KOVAN_ENDPOINT if 'kovan' in version else MAINNET_ENDPOINT
        self.web3 = Web3(Web3.HTTPProvider(endpoint))

    def load_contracts(self):
        print("Loading contracts")
        self.extractor = Extractor(self.base_url)
        print("Contracts loaded")

    def get_contract(self, contract_name):
        if not self.extractor:
            print("Load contracts first")
            return None

        address = self.extractor.addresses.get(contract_name)
        abi = self.extractor.contracts.get(contract_name)
        if address and abi:
            return self.web3.eth.contract(address=address, abi=abi)
        
        print(f"Address or ABI not found for {contract_name}")
        return None
        
    
if __name__ == "__main__":
    e = Ethercraft()
    e.load_contracts()
    contract = e.get_contract('character')
    inventory_integer = contract.caller.viewInventory(13)
    print(inventory_integer)
