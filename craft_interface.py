import os
from dotenv import load_dotenv
load_dotenv()
import contract.whirlpool as whirlpool
import contract.equipment as equipment
import contract.character as character
from util import get_micro

KOVAN_ENDPOINT = os.getenv('KOVAN_ENDPOINT')
WHIRLPOOL_ADDRESS = os.getenv('WHIRLPOOL_ADDRESS')
EQUIPMENT_ADDRESS = os.getenv('EQUIPMENT_ADDRESS')
CHARACTER_ADDRESS = os.getenv('CHARACTER_ADDRESS')
MAINNET_ENDPOINT = os.getenv('MAINNET_ENDPOINT')

from web3 import Web3

def whirlpool_contract():
    w3 = Web3(Web3.HTTPProvider(MAINNET_ENDPOINT))

    return w3.eth.contract(address=WHIRLPOOL_ADDRESS, abi=whirlpool.abi)

def equipment_contract():
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    return w3.eth.contract(address=EQUIPMENT_ADDRESS, abi=equipment.abi)

def get_inventory(id):
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))
    contract = w3.eth.contract(address=CHARACTER_ADDRESS, abi=character.abi)

    inventory_integer = contract.caller.viewInventory(id)
    retval = ""
    for i in range(3, 78, 5):
        item_id = get_micro(inventory_integer, i, 3)
        item_count = get_micro(inventory_integer, i + 2, 2)
        if item_id:
            retval += f"item id: {item_id}\t - count:{item_count}\n"
    return retval

def get_equipment(id):
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))
    contract = w3.eth.contract(address=CHARACTER_ADDRESS, abi=character.abi)

    equipment_integer = contract.caller.viewEquipment(id)
    equipment_sets = [
        ('HELMET', 3, 3),
        ('CHEST', 6, 3),
        ('LOWER', 9, 3),
        ('BOOTS', 12, 3),
        ('LHAND', 27, 3),
        ('RHAND', 30, 3),
        ('GLOVES', 63, 3),
        ('LWRIST', 33, 3),
        ('RWRIST', 36, 3),
        ('AMULET', 15, 3),
        ('WAIST', 18, 3),
        ('CLOAK', 21, 3),
        ('BACKPACK', 24, 3),
        ('LRING1', 39, 3),
        ('RRING1', 42, 3),
        ('LRING2', 45, 3),
        ('RRING2', 48, 3),
        ('LRING3', 51, 3),
        ('RRING3', 54, 3),
        ('LRING4', 57, 3),
        ('RRING4', 60, 3)
    ]
    retval = ""
    for equipment in equipment_sets:
        equipment_id = get_micro(equipment_integer, equipment[1], equipment[2])
        if equipment_id:
            retval += f"{equipment_id} equipped on {equipment[0]}\n"
    return retval
    