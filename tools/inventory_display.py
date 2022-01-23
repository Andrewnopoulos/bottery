import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ethercraft.types import Inventory
from ethercraft import ItemDatabase

SCALE_FACTOR = 2
FONT = ImageFont.truetype('tools/static/PTM55FT.ttf', 28)
IMAGE_WIDTH = 700
IMAGE_HEIGHT = 36
ICON_DIMENSIONS = 32

OUTPUT_DIRECTORY = 'tools/temp'

if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

class InventoryRenderer():
    def __init__(self, item_database: ItemDatabase):
        self.itemdb = item_database

    def create_inventory_image(self, inventory: Inventory):

        base = Image.open('tools/static/inventory_background.png')
        db = self.itemdb.items
        
        item_images = []

        for i in inventory.items:
            base_copy = base.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.NEAREST)
            
            translations = {}
            if db[i] and db[i].get('png_path'):
                item_img = Image.open(db[i].get('png_path'))
                item_img = item_img.resize((ICON_DIMENSIONS, ICON_DIMENSIONS), Image.NEAREST)
                base_copy.paste(item_img, (2, 2), item_img)
                translations = self.itemdb.get_translations(i)
            else:
                continue

            draw = ImageDraw.Draw(base_copy)
            draw.text((ICON_DIMENSIONS + 6, 2), translations.get('name', 'missing_name'), (0, 0, 0), font=FONT)
            draw.text((IMAGE_WIDTH - 4, 2), f'x{str(inventory.items[i])}', (0, 0, 0), font=FONT, anchor='ra')
            item_images.append(base_copy)

        output_image_dimensions = (IMAGE_WIDTH, len(item_images) * IMAGE_HEIGHT)
        output_image = Image.new('RGB', output_image_dimensions, (0, 0, 0))
        for index, image in enumerate(item_images):
            paste_position = (0, index * IMAGE_HEIGHT)
            output_image.paste(image, paste_position)

        filename = OUTPUT_DIRECTORY + '/inventory_done.png'
        output_image.save(filename, quality=95)
        return filename


if __name__ == '__main__':
    from craft_interface import BotInterface

    bot = BotInterface()
    bot.ec.items

    renderer = InventoryRenderer(bot.ec.items)

    renderer.create_inventory_image(bot.get_inventory(10))