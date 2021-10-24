import os
from dotenv import load_dotenv
load_dotenv()
import contract.whirlpool as whirlpool
import contract.equipment as equipment
import contract.character as character
import contract.dungeon as dungeon
import contract.combat as combat
from util import get_micro
from data.db import get_itemdb, get_translations
from data.inventory import Inventory
from data.events.parser import parse_events

KOVAN_ENDPOINT = os.getenv('KOVAN_ENDPOINT')
WHIRLPOOL_ADDRESS = os.getenv('WHIRLPOOL_ADDRESS')
EQUIPMENT_ADDRESS = os.getenv('EQUIPMENT_ADDRESS')
CHARACTER_ADDRESS = os.getenv('CHARACTER_ADDRESS')
MAINNET_ENDPOINT = os.getenv('MAINNET_ENDPOINT')
DUNGEON_ADDRESS = os.getenv('DUNGEON_ADDRESS')
COMBAT_ADDRESS = os.getenv('COMBAT_ADDRESS')

from web3 import Web3

def whirlpool_contract():
    w3 = Web3(Web3.HTTPProvider(MAINNET_ENDPOINT))

    return w3.eth.contract(address=WHIRLPOOL_ADDRESS, abi=whirlpool.abi)

def equipment_contract():
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    return w3.eth.contract(address=EQUIPMENT_ADDRESS, abi=equipment.abi)

def initialise_itemdb():
    get_itemdb()

def dungeon_contract():
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    return w3.eth.contract(address=DUNGEON_ADDRESS, abi=dungeon.abi)

def character_contract():
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    return w3.eth.contract(address=CHARACTER_ADDRESS, abi=character.abi)

def combat_contract():
    w3 = Web3(Web3.HTTPProvider(KOVAN_ENDPOINT))

    return w3.eth.contract(address=COMBAT_ADDRESS, abi=combat.abi)

def get_inventory(id):
    contract = character_contract()

    inventory_integer = contract.caller.viewInventory(id)
    inventory = Inventory()
    for i in range(3, 78, 5):
        item_id = get_micro(inventory_integer, i, 3)
        item_count = get_micro(inventory_integer, i + 2, 2)
        inventory.add_items(item_id, item_count)
        # if item_id:
        #     desc = f"item id: {item_id}"
        #     if itemdb[item_id]:
        #         item_info = get_translations(itemdb[item_id])
        #         if item_info:
        #             desc = f"{item_info.get('name', 'unknown_name')}, {item_info.get('description', 'unknown_description')}"
        #     retval += f"{desc}\n\t\tcount: {item_count}\n"
    return inventory

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
    

def get_run_info(run_ids):
    dungeon_contract_instance = dungeon_contract()
    combat_contract_instance = combat_contract()

    dungeon_events = [
        dungeon_contract_instance.events.FloorEntered,
        dungeon_contract_instance.events.EnteredRoom,
        dungeon_contract_instance.events.EffectEncountered,
        dungeon_contract_instance.events.EnemyEncountered,
        dungeon_contract_instance.events.TrapEncountered,
        dungeon_contract_instance.events.LootEncountered,
        dungeon_contract_instance.events.CreditsEncountered,
        dungeon_contract_instance.events.ExperienceGained
    ]

    combat_events = [
        combat_contract_instance.events.CombatEvent
    ]

    all_entries = []

    for event in dungeon_events:
        print(f"event: {event.event_name}")
        filter = event.createFilter(
            fromBlock='0x0',
            argument_filters={"_run": run_ids}
        )
        for i in filter.get_all_entries():
            all_entries.append(i)

    for event in combat_events:
        print(f"event: {event.event_name}")
        filter = event.createFilter(
            fromBlock='0x0',
            argument_filters={"_runID": run_ids}
        )
        for i in filter.get_all_entries():
            all_entries.append(i)

    all_entries.sort(key=lambda x: x['logIndex'])

    return all_entries

async def view_runs():
    contract = character_contract()

    for i in range(20):
        print( f"{i} - {contract.caller.viewRuns(i)}" )

if __name__ == '__main__':
    contract = character_contract()

    # contract.caller.viewRuns(10)
    # # print(contract)
    # import asyncio
    # asyncio.run(view_runs())

    # get_run_info(contract.caller.viewRuns(5))