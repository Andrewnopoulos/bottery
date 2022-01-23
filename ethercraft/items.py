import os

from ethercraft.scraping.extractor import Extractor
from ethercraft.static.itemdb_extra import add_extra_items

class ItemDatabase():

    def __init__(self, extractor):
        self.items = []
        self.populated = False
        self.extractor = extractor

    def _populate_icon_paths(self):
        item_icon_list = self.extractor.icons.icon_array
        if not item_icon_list:
            print("WARNING: item icon list is empty")
            return
        for item_idx, icon_png in item_icon_list:
            idx = int(item_idx)
            icon_png = os.path.basename(icon_png)
            if idx < len(self.items) and self.items[idx] is not None:
                self.items[idx]['png'] = icon_png
                self.items[idx]['png_path'] = 'ethercraft/scraping/icons/' + icon_png

    def load_from_extractor(self):
        try:
            self.items = self.extractor.load_db_from_js('itemDB.js')
            add_extra_items(self.items)
            self._populate_icon_paths()
            
            self.populated = True
        except Exception as err:
            print(f"error while populating item database:\n{str(err)}")

        return self.populated

    def get_translations(self, index, lang='EN'):
        try:
            translation_list = self.items[index].get('strings')
            for translation in translation_list:
                if translation.get('lang') == lang:
                    return translation
        except:
            print(f"Item not found at index {index}")
        return {}

if __name__ == '__main__':
    extractor = Extractor('https://ethercraft.io/kovan_v46/')

    items = ItemDatabase(extractor)
    items.load_from_extractor()

    print(items.items)