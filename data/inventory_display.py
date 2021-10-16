from os import scandir
from PIL import Image
from data.inventory import Inventory

from data.itemdb import get_itemdb

SCALE_FACTOR = 2

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
    create_inventory_image(get_inventory(10))