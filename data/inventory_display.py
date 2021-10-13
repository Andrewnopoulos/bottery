from PIL import Image
from data.inventory import Inventory

from data.itemdb import get_itemdb

def create_inventory_image(inventory: Inventory):
    base = Image.open('data/static/inventory.png')
    # print (base.info['icc_profile'])
    base_copy = base.copy()

    db = get_itemdb()

    x = 25
    y = 35
    for i in inventory.items:
        if db[i] and db[i].get('png_path'):
            item_img = Image.open(db[i].get('png_path'))
            base_copy.paste(item_img, (x, y), item_img)
            x += 57
            if x > 150:
                x = 25
                y += 51
            if y > 90:
                break

    output_filename = 'data/static/inventory_done.png'

    base_copy.save(output_filename, quality=95)
    return output_filename

    # im1 = Image.open('data/src/rocket.jpg')
    # im2 = Image.open('data/src/lena.jpg')

    # back_im = im1.copy()
    # back_im.paste(im2, (100, 50))
    # back_im.save('data/dst/rocket_pillow_paste.jpg', quality=95)

from craft_interface import get_inventory

create_inventory_image(get_inventory(10))