from os import scandir
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from data.inventory import Inventory

from data.itemdb import get_itemdb, get_translations

SCALE_FACTOR = 2
FONT = ImageFont.truetype('data/static/PTM55FT.ttf', 28)
IMAGE_WIDTH = 700
IMAGE_HEIGHT = 36
ICON_DIMENSIONS = 32

def create_inventory_image_new(inventory: Inventory):
    base = Image.open('data/static/inventory_background.png')
    db = get_itemdb()

    item_images = []

    for i in inventory.items:
        base_copy = base.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.NEAREST)
        
        translations = {}
        if db[i] and db[i].get('png_path'):
            item_img = Image.open(db[i].get('png_path'))
            item_img = item_img.resize((ICON_DIMENSIONS, ICON_DIMENSIONS), Image.NEAREST)
            base_copy.paste(item_img, (2, 2), item_img)
            translations = get_translations(db[i])
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

    filename = 'data/static/inventory_done.png'
    output_image.save(filename, quality=95)
    return filename

def create_inventory_image(inventory: Inventory):
    base = Image.open('data/static/inventory.png')
    base_copy = base.copy()

    db = get_itemdb()

    xoffset = 26
    xiteration = 57
    yoffset = 35
    yiteration = 50

    newsize = (base_copy.width * SCALE_FACTOR, base_copy.height * SCALE_FACTOR)
    base_copy = base_copy.resize(newsize, Image.NEAREST)

    x = xoffset * SCALE_FACTOR
    y = yoffset * SCALE_FACTOR
    for i in inventory.items:
        if db[i] and db[i].get('png_path'):
            item_img = Image.open(db[i].get('png_path'))
            newsize = (item_img.width * SCALE_FACTOR, item_img.height * SCALE_FACTOR)
            item_img = item_img.resize(newsize, Image.NEAREST)
            base_copy.paste(item_img, (x, y), item_img)
            x += xiteration * SCALE_FACTOR
            if x > (xoffset * SCALE_FACTOR) + 2 * (xiteration * SCALE_FACTOR):
                x = xoffset * SCALE_FACTOR
                y += yiteration * SCALE_FACTOR
            if y > (yoffset * SCALE_FACTOR) + 3 * (yiteration * SCALE_FACTOR):
                break

    output_filename = 'data/static/inventory_done.png'

    base_copy.save(output_filename, quality=95)
    return output_filename


if __name__ == '__main__':
    from craft_interface import get_inventory
    create_inventory_image_new(get_inventory(10))