import os
import json
from pathlib import Path

from data.static.itemdb_extra import add_extra_items
from data.icons import fetch_icons

itemdb = [None] * 1000

def get_translations(item, lang='EN'):
    translation_list = item.get('strings')
    for translation in translation_list:
        if translation.get('lang') == lang:
            return translation
    return {}

def get_itemdb():
    if not itemdb[0]:
        itemdb_path = Path('data') / 'static'
        with open(itemdb_path / "itemdb.json", 'r') as db_file:
            data = json.load(db_file)
            for idx, val in enumerate(data):
                itemdb[idx] = val

        add_extra_items(itemdb)

        item_icon_list = fetch_icons()
        for item_idx, icon_png in item_icon_list:
            idx = int(item_idx)
            icon_png = os.path.basename(icon_png)
            if idx < len(itemdb) and itemdb[idx] is not None:
                itemdb[idx]['png'] = icon_png
                itemdb[idx]['png_path'] = Path('data/img') / icon_png
        
    return itemdb
