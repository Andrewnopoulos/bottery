import os
import json
from pathlib import Path

from data.static.itemdb_extra import add_extra_items
from data.icons import fetch_icons

_itemdb = [None] * 1000
_beastdb = [None] * 6

def get_translations(item, lang='EN'):
    translation_list = item.get('strings')
    for translation in translation_list:
        if translation.get('lang') == lang:
            return translation
    return {}

def get_beastdb():
    if not _beastdb[0]:
        beastdb_path = Path('data') / 'static'
        with open(beastdb_path / 'bestiarydb.json', 'r') as db_file:
            data = json.load(db_file)
            for idx, val in enumerate(data):
                _beastdb[idx] = val
    return _beastdb

def get_itemdb():
    if not _itemdb[0]:
        itemdb_path = Path('data') / 'static'
        with open(itemdb_path / "itemdb.json", 'r') as db_file:
            data = json.load(db_file)
            for idx, val in enumerate(data):
                _itemdb[idx] = val

        add_extra_items(_itemdb)

        item_icon_list = fetch_icons()
        for item_idx, icon_png in item_icon_list:
            idx = int(item_idx)
            icon_png = os.path.basename(icon_png)
            if idx < len(_itemdb) and _itemdb[idx] is not None:
                _itemdb[idx]['png'] = icon_png
                _itemdb[idx]['png_path'] = Path('data/img') / icon_png
        
    return _itemdb


if __name__ == '__main__':

    beast_db = get_beastdb()

