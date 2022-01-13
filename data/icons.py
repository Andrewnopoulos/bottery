import os
import requests
import re
from pathlib import Path

# ICONS_URL = os.getenv('ICONS_URL')
ETHERCRAFT_KOVAN_URL = "https://ethercraft.io/kovan_v46/"
ICONS_URL = ETHERCRAFT_KOVAN_URL + "css/icons.css"

def parse_raw_icon_response(raw_icon_response):
    matches = re.findall(r'.item-(\d+){background-image:url\(../img/([/a-z_A-Z]*.png)\)}', raw_icon_response)
    return matches

def fetch_icons():
    icon_array = []
    req = requests.get(ICONS_URL)
    if req.status_code == 200:
        raw_icon_list = req.text
        icon_array = parse_raw_icon_response(raw_icon_list)

    return icon_array

def download_icon_png(icon_name):
    icon_path = ETHERCRAFT_KOVAN_URL + 'img/' + icon_name
    if '/' in icon_name:
        icon_name = os.path.basename(icon_name)
    local_image_path = Path('data') / 'img' / icon_name
    if os.path.exists(local_image_path):
        return
    req = requests.get(icon_path)
    if req.status_code == 200:
        with open(local_image_path, 'wb') as img:
            img.write(req.content)

def download_all_icons():
    item_icon_list = fetch_icons()
    for item_idx, icon_png in item_icon_list:
        download_icon_png(icon_png)

if __name__ == '__main__':
    download_all_icons()