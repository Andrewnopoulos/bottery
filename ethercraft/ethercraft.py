import os
from dotenv import load_dotenv

from ethercraft.scraping.contract_extractor import Extractor
load_dotenv()

ETHERCRAFT_VERSION = os.getenv('ETHERCRAFT_VERSION')
ETHERCRAFT_URL = os.getenv('ETHERCRAFT_URL')

class Ethercraft():

    def __init__(self, version=ETHERCRAFT_VERSION):
        self.base_url = ETHERCRAFT_URL + version + '/'

    def load_contracts(self):
        extractor = Extractor(self.base_url)
        

    
