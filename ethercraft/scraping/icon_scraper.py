import os
import requests
import re
from pathlib import Path

class IconScraper():
    def __init__(self, ethercraft_url):
        self.ec_url = ethercraft_url
        self.icons_url = ethercraft_url + "css/icons.css"
        self.icon_array = self.fetch_icons()

    def parse_raw_icon_response(self, raw_icon_response):
        matches = re.findall(r'.item-(\d+){background-image:url\(../img/([/a-z_A-Z]*.png)\)}', raw_icon_response)
        return matches

    def fetch_icons(self):
        icon_array = []
        req = requests.get(self.icons_url)
        if req.status_code == 200:
            raw_icon_list = req.text
            icon_array = self.parse_raw_icon_response(raw_icon_list)

        return icon_array

    def download_icon_png(self, icon_name):
        icon_path = self.ec_url + 'img/' + icon_name
        if '/' in icon_name:
            icon_name = os.path.basename(icon_name)
        local_image_path = Path('ethercraft') / 'scraping' / 'icons' / icon_name
        if os.path.exists(local_image_path):
            return
        req = requests.get(icon_path)
        if req.status_code == 200:
            with open(local_image_path, 'wb') as img:
                img.write(req.content)

    def download_all_icons(self):
        for item_idx, icon_png in self.icon_array:
            self.download_icon_png(icon_png)

if __name__ == '__main__':
    scraper = IconScraper("https://ethercraft.io/kovan_v46/")

    scraper.download_all_icons()