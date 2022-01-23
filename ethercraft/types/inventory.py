
class Inventory():

    def __init__(self):
        self.items = {}

    def add_items(self, item_index, item_count):
        self.items[item_index] = item_count